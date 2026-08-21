#!/usr/bin/env bash
#
# 補上 soma-agent.com 收信需要的 DNS：三筆 Cloudflare Email Routing 的 MX + 一筆 SPF。
#
#   export CF_API_TOKEN=<Zone:DNS:Edit 權限的 token>
#   bash scripts/setup-dns-mail.sh --dry-run   # 先看要做什麼
#   bash scripts/setup-dns-mail.sh             # 真的建立
#
# 只新增缺的記錄，已存在的略過；SPF 若已有會印出現值要你自己確認，不會蓋掉。
# token 只從環境變數讀，不接受命令列參數（`ps` 看得到 arg，會外洩）。

set -uo pipefail

ZONE_NAME="soma-agent.com"
API="https://api.cloudflare.com/client/v4"
DRY_RUN=false
[ "${1:-}" = "--dry-run" ] && DRY_RUN=true

# Brevo 負責寄（序號信），Cloudflare Email Routing 負責收（support@ 轉寄）。
# 兩個 include 都要在，少了 Brevo 那個，序號信在 Gmail 會被打成垃圾郵件。
SPF_VALUE="v=spf1 include:spf.brevo.com include:_spf.mx.cloudflare.net ~all"

: "${CF_API_TOKEN:?請先 export CF_API_TOKEN（Zone → DNS → Edit 權限）}"

api() {
  curl -s -H "Authorization: Bearer ${CF_API_TOKEN}" -H "Content-Type: application/json" "$@"
}

ok_or_die() {
  local json="$1" what="$2"
  if ! printf '%s' "$json" | python3 -c "import json,sys; sys.exit(0 if json.load(sys.stdin).get('success') else 1)"; then
    echo "✗ ${what} 失敗："
    printf '%s' "$json" | python3 -m json.tool 2>/dev/null | head -20
    exit 1
  fi
}

echo "查詢 zone…"
ZONE_JSON=$(api "${API}/zones?name=${ZONE_NAME}")
ok_or_die "$ZONE_JSON" "查詢 zone"
ZONE_ID=$(printf '%s' "$ZONE_JSON" | python3 -c "
import json,sys
z=json.load(sys.stdin)['result']
if not z: print(''); sys.exit()
print(z[0]['id'])")
[ -n "$ZONE_ID" ] || { echo "✗ 這個 token 看不到 ${ZONE_NAME}（權限的 zone 選錯？）"; exit 1; }
echo "  zone id: ${ZONE_ID:0:8}…"

EXISTING=$(api "${API}/zones/${ZONE_ID}/dns_records?per_page=200")
ok_or_die "$EXISTING" "列出現有記錄"

# 既有 SPF 不覆蓋：可能有人手動調過，蓋掉會讓寄信突然開始被退
CURRENT_SPF=$(printf '%s' "$EXISTING" | python3 -c "
import json,sys
for r in json.load(sys.stdin)['result']:
    if r['type']=='TXT' and 'v=spf1' in r.get('content',''):
        print(r['content']); break")

create() {
  local type="$1" name="$2" content="$3" priority="${4:-}"
  local exists
  exists=$(printf '%s' "$EXISTING" | python3 -c "
import json,sys
t,n,c=sys.argv[1],sys.argv[2],sys.argv[3]
for r in json.load(sys.stdin)['result']:
    if r['type']==t and r['name']==n and c.strip('\"') in r.get('content','').strip('\"'):
        print('yes'); break
" "$type" "$ZONE_NAME" "$content")
  if [ "$exists" = "yes" ]; then
    echo "  — 已存在，略過：${type} ${content}"
    return 0
  fi
  if $DRY_RUN; then
    echo "  + [dry-run] ${type} ${ZONE_NAME} → ${content}${priority:+（優先 ${priority}）}"
    return 0
  fi
  local body
  if [ -n "$priority" ]; then
    body=$(python3 -c "
import json,sys
print(json.dumps({'type':sys.argv[1],'name':sys.argv[2],'content':sys.argv[3],'priority':int(sys.argv[4]),'ttl':1}))
" "$type" "$ZONE_NAME" "$content" "$priority")
  else
    body=$(python3 -c "
import json,sys
print(json.dumps({'type':sys.argv[1],'name':sys.argv[2],'content':sys.argv[3],'ttl':1}))
" "$type" "$ZONE_NAME" "$content")
  fi
  local res
  res=$(api -X POST "${API}/zones/${ZONE_ID}/dns_records" --data "$body")
  ok_or_die "$res" "建立 ${type} ${content}"
  echo "  ✓ 已建立：${type} ${content}${priority:+（優先 ${priority}）}"
  return 0
}

echo
echo "MX（Cloudflare Email Routing）"
create MX "$ZONE_NAME" "route1.mx.cloudflare.net" 1
create MX "$ZONE_NAME" "route2.mx.cloudflare.net" 95
create MX "$ZONE_NAME" "route3.mx.cloudflare.net" 96

echo
echo "SPF"
if [ -n "$CURRENT_SPF" ]; then
  echo "  ! 已有 SPF，沒有動它：${CURRENT_SPF}"
  case "$CURRENT_SPF" in
    *spf.brevo.com*) ;;
    *) echo "    ⚠ 這條缺 include:spf.brevo.com —— 序號信會被打成垃圾郵件，請手動補上" ;;
  esac
  case "$CURRENT_SPF" in
    *_spf.mx.cloudflare.net*) ;;
    *) echo "    ⚠ 這條缺 include:_spf.mx.cloudflare.net —— 轉寄的信可能被退，請手動補上" ;;
  esac
else
  create TXT "$ZONE_NAME" "$SPF_VALUE"
fi

echo
if $DRY_RUN; then
  echo "以上是 dry-run，什麼都沒改。拿掉 --dry-run 才會實際建立。"
else
  echo "完成。DNS 生效後驗證："
  echo "  dig +short MX soma-agent.com"
  echo "  dig +short TXT soma-agent.com | grep spf1"
  echo
  echo "接著到 Cloudflare → Email Routing 確認 support@soma-agent.com 的轉寄規則是啟用狀態，"
  echo "然後從外部信箱寄一封測試信。"
fi
