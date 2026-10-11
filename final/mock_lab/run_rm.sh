#!/usr/bin/env bash
# รัน RapidMiner process (.rmp) แบบไม่เปิดหน้าจอ (batch) — ใช้ตรวจว่าไฟล์ที่สร้างรันได้จริง
#
# ข้อจำกัด 2 อย่างของ ai-studio-batch.sh ที่สคริปต์นี้แก้ให้:
#  1) ต้องใช้ Java 17 — ตัวรัน batch เรียก System.setSecurityManager() ซึ่ง Java 21 ห้าม/Java 25 ลบแล้ว
#     (GUI ปกติไม่มีปัญหานี้ ใช้ Java ตัวไหนก็ได้)
#  2) สคริปต์ใช้ eval → path ที่มีช่องว่าง ("data mining") ถูกตัดคำ → คัดลอกไปไว้ที่ path ไม่มีช่องว่างก่อน
#
# ใช้:  bash final/mock_lab/run_rm.sh final/mock_lab/recipes/*.rmp
set -u
RM="$HOME/App/ai-studio-2026.1.1/Altair/RapidMiner/AI Studio 2026.1.1"
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
TMP=/tmp/rmbatch          # โฟลเดอร์ทำงานชั่วคราว (ไฟล์ข้างในถูกเขียนทับทุกครั้ง)
mkdir -p "$TMP"
fail=0
for f in "$@"; do
  name=$(basename "$f")
  safe="$TMP/$(echo "$name" | tr ' ' '_')"
  cp "$f" "$safe"
  log="$TMP/log.txt"
  ( cd "$TMP" && timeout 600 bash "$RM/scripts/ai-studio-batch.sh" -f "$safe" ) >"$log" 2>&1
  # batch runner คืนค่า 0 แม้ process พัง → ดูข้อความ error จริงใน log
  # (ข้อความ license / certificate / Python extension เป็นแค่คำเตือนตอนเปิดโปรแกรม ไม่นับ)
  errs=$(grep -E "Process failed|UserError|Error in|Cannot read process|XMLException|OperatorCreationException|ProcessSetupError|Exception:" "$log" \
         | grep -vE "AltairLicense|certificate|AccessControlException|license settings|^\s*at " | head -6)
  if [ -n "$errs" ]; then
    echo "  ✗ $name"; echo "$errs" | sed 's/^/      /'; fail=1
  else
    echo "  ✓ $name"
  fi
done
exit $fail
