Readme
==========================
git clone https://github.com/magicwenli/bili-sofa.git

cd bili-sofa

touch .secrets.yaml

cat > .secrets.yaml<< EOF
credential:
  sessdata: YOUR_SESSDATA
  bili_jct: YOUR_BILI_JCT
  buvid3: YOUR_BUVID3
wxpusher:
  uids:
    - ''
  topic_ids: 
    - ''
  token: ''
EOF

pip install bilibili-api wxpusher

python main.py