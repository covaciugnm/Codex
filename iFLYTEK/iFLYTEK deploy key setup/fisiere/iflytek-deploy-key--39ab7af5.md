---
name: iflytek-deploy-key
description: "Deploy key read-only pentru repo GitHub covaciugnm/iFLYTEK, creat 31.10.2026, cheia privata in C:\\Users\\User\\.ssh\\iflytek_deploy_20261031"
metadata:
  node_type: memory
  type: reference
  originSessionId: 1ecce1c4-369b-4e21-8511-407d9123d618
  modified: 2026-10-31T09:34:46.253Z
---

Repo GitHub: covaciugnm/iFLYTEK — deploy keys: https://github.com/covaciugnm/iFLYTEK/settings/keys

- Title: `iFLYTEK deploy - 2026-10-31`
- Acces: doar citire (read-only, nu poate face push)
- Cheia privata: `C:\Users\User\.ssh\iflytek_deploy_20261031` (publica: `C:\Users\User\.ssh\iflytek_deploy_20261031.pub`)
- Cheia publica: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICnvdpGef8Xvf6j5NzOrW1+BCg70CFJZ88OfXxN43OWG`

**How to apply:** pentru clone/pull din iFLYTEK foloseste
`GIT_SSH_COMMAND="ssh -i C:/Users/User/.ssh/iflytek_deploy_20261031 -o IdentitiesOnly=yes" git clone git@github.com:covaciugnm/iFLYTEK.git`
Pentru push e nevoie de alta cheie (cu write access). Vezi si [[github-repos-site-uri]].
