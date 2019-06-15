Description=Sygnaller registry daemon

Wants=network.target
After=syslog.target network-online.target

[Service]
Type=simple
ExecStart=python2.7 /home/ubuntu/registryd/main.py
Restart=on-failure
RestartSec=10
KillMode=process

[Install]
WantedBy=multi-user.target