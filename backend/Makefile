install:
	ansible-galaxy install -r requirements.yml

deploy:
	docker buildx build --platform linux/amd64 -t arhangel662/speakfluentai:latest --push . && ansible-playbook playbook.yml -i inventory.ini --ask-vault-password

vault edit:
	ansible-vault edit group_vars/webservers/vault.yml





