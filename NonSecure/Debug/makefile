################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include Drivers/STM32L5xx_HAL_Driver/Src/subdir.mk
-include Core/Startup/subdir.mk
-include Core/Src/subdir.mk
-include subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

# Add inputs and outputs from these tool invocations to the build variables 
EXECUTABLES += \
TrustZone-ToggleLED_NonSecure.elf \

SIZE_OUTPUT += \
default.size.stdout \

OBJDUMP_LIST += \
TrustZone-ToggleLED_NonSecure.list \

OBJCOPY_BIN += \
TrustZone-ToggleLED_NonSecure.bin \


# All Target
all: TrustZone-ToggleLED_NonSecure.elf secondary-outputs

# Tool invocations
TrustZone-ToggleLED_NonSecure.elf: $(OBJS) $(USER_OBJS) /Users/windy/STM32CubeIDE/workspace_1.3.0/TrustZone-ToggleLED/NonSecure/STM32L552ZETXQ_FLASH.ld
	arm-none-eabi-gcc -o "TrustZone-ToggleLED_NonSecure.elf" @"objects.list" $(USER_OBJS) $(LIBS) -mcpu=cortex-m33 -T"/Users/windy/STM32CubeIDE/workspace_1.3.0/TrustZone-ToggleLED/NonSecure/STM32L552ZETXQ_FLASH.ld" --specs=nosys.specs -Wl,-Map="TrustZone-ToggleLED_NonSecure.map" -Wl,--gc-sections -static --specs=nano.specs -mfpu=fpv5-sp-d16 -mfloat-abi=hard -mthumb -Wl,--start-group -lc -lm -Wl,--end-group
	@echo 'Finished building target: $@'
	@echo ' '

default.size.stdout: $(EXECUTABLES)
	arm-none-eabi-size  $(EXECUTABLES)
	@echo 'Finished building: $@'
	@echo ' '

TrustZone-ToggleLED_NonSecure.list: $(EXECUTABLES)
	arm-none-eabi-objdump -h -S $(EXECUTABLES) > "TrustZone-ToggleLED_NonSecure.list"
	@echo 'Finished building: $@'
	@echo ' '

TrustZone-ToggleLED_NonSecure.bin: $(EXECUTABLES)
	arm-none-eabi-objcopy  -O binary $(EXECUTABLES) "TrustZone-ToggleLED_NonSecure.bin"
	@echo 'Finished building: $@'
	@echo ' '

# Other Targets
clean:
	-$(RM) *
	-@echo ' '

secondary-outputs: $(SIZE_OUTPUT) $(OBJDUMP_LIST) $(OBJCOPY_BIN)

.PHONY: all clean dependents
.SECONDARY:

-include ../makefile.targets
