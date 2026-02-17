chown -R "root:root" /data 2>/dev/null || true
chown -R "claw:claw" /data/openclaw-data/workspace-* 2>/dev/null || true
chown -R "claw:claw" /data/openclaw-data/openclaw.json 2>/dev/null || true
chown -R "claw:claw" /data/openclaw-data/skills 2>/dev/null || true
chown -R "claw:claw" /data/workspace 2>/dev/null || true

chown -R "claw:claw" /data/.openclaw 2>/dev/null || true
chown -R "claw:claw" /data/.cache 2>/dev/null || true
chown -R "claw:claw" /data/.git-credentials 2>/dev/null || true
chown -R "claw:claw" /data/.npm 2>/dev/null || true
chown -R "claw:claw" /data/.pki 2>/dev/null || true