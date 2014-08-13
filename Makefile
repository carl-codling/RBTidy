USER_PLUGIN_DIR = ~/.local/share/rhythmbox/plugins/RBTidy/
SYSTEM_PLUGIN_DIR = /usr/lib/rhythmbox/plugins/RBTidy/
SYSTEM64_PLUGIN_DIR = /usr/lib64/rhythmbox/plugins/RBTidy/

install: 
	@echo "Installing plugin files to $(USER_PLUGIN_DIR) ..."
	@rm -r -f $(USER_PLUGIN_DIR)
	@mkdir -p $(USER_PLUGIN_DIR)
	@cp ./RBTidy.plugin $(USER_PLUGIN_DIR)
	@cp ./RBTidy.py $(USER_PLUGIN_DIR)
	@echo "Done!"

install-systemwide: 
	@if [ -d "$(SYSTEM_PLUGIN_DIR)rb" ]; then \
		echo "Installing plugin files to $(SYSTEM_PLUGIN_DIR) ..."; \
		sudo rm -r -f $(SYSTEM_PLUGIN_DIR); \
		sudo mkdir -p $(SYSTEM_PLUGIN_DIR); \
		sudo cp ./RBTidy.plugin $(USER_PLUGIN_DIR) \
		sudo cp ./RBTidy.py $(USER_PLUGIN_DIR) \
	else \
		echo "Installing plugin files to $(SYSTEM64_PLUGIN_DIR) ..."; \
		sudo rm -r -f $(SYSTEM64_PLUGIN_DIR); \
		sudo mkdir -p $(SYSTEM64_PLUGIN_DIR); \
		sudo cp ./RBTidy.plugin $(SYSTEM64_PLUGIN_DIR) \
		sudo cp ./RBTidy.py $(SYSTEM64_PLUGIN_DIR) \
	fi
	@echo "Done!"#


uninstall:
	@echo "Removing plugin files..."
	@rm -r -f $(USER_PLUGIN_DIR)
	@sudo rm -r -f $(SYSTEM_PLUGIN_DIR)
	@sudo rm -r -f $(SYSTEM64_PLUGIN_DIR)
	@echo "Done!"
