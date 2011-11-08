ARDUINO_DIR  = /usr/share/arduino
AVR_TOOLS_PATH    = /usr/bin

TARGET       = kdrvario
ARDUINO_LIBS = Wire LiquidCrystal

MCU          = atmega328p
F_CPU        = 16000000
ARDUINO_PORT = /dev/ttyACM0

AVRDUDE_ARD_PROGRAMMER=arduino
AVRDUDE_ARD_BAUDRATE=115200
AVRDUDE_CONF   = /etc/avrdude.conf

#include /usr/share/arduino/Arduino.mk

include Arduino.mk

SYS_INCLUDES := -I$(ARDUINO_LIB_PATH)/Wire/utility/ $(SYS_INCLUDES)
LIB_SRC := $(ARDUINO_LIB_PATH)/Wire/utility/twi.c $(LIB_SRC)
LIB_OBJS := $(patsubst $(ARDUINO_LIB_PATH)/%.c,$(OBJDIR)/libs/%.o,$(LIB_OBJS))

$(OBJDIR)/libs/%.o: $(ARDUINO_LIB_PATH)/%.c
	mkdir -p $(dir $@)
	$(CC) -c $(CPPFLAGS) $(CFLAGS) $< -o $@

debug:
	echo LIB_SRC= $(LIB_SRC)
	echo DDD: $(LIB_OBJS)
	#echo GGG: $(patsubst $(ARDUINO_LIB_PATH)/%.cpp,$(OBJDIR)/libs/%.o,$(LIB_SRC))
	echo OBJS: $(OBJS)
	echo TARGET_ELF $(TARGET_ELF)

$(TARGET_ELF): 	$(OBJS)
		$(CC) $(LDFLAGS) -o $@ $(OBJS) $(SYS_OBJS)

# firmware switch targets
fw_switch_pressure_log: total_clean
	ln -sf pde/pressure_log.pde firmware.pde

fw_switch_sound_check: total_clean
	ln -sf pde/sound_check.pde firmware.pde

fw_switch_stats: total_clean
	ln -sf pde/stats.pde firmware.pde

fw_switch_rencoder: total_clean
	ln -sf pde/rencoder.pde firmware.pde

total_clean:
	rm -rf build-cli
