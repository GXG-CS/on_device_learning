
#
# Main component of TF Micro project 'micro_speech'.
#

idf_component_register(
    SRCS main.cc  model_data.cc model_runner.cc gattc_comm.cc
    PRIV_REQUIRES spi_flash
    INCLUDE_DIRS ""
    PRIV_REQUIRES esp_timer nvs_flash bt)


# Add the compiler flags to relax warnings
target_compile_options(${COMPONENT_LIB} PRIVATE -Wno-error=switch -Wno-error=jump-misses-init)