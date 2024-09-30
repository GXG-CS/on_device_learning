
#
# Main component of TF Micro project 'micro_speech'.
#

idf_component_register(
    SRCS main.cc model_data.cc data_sender.cc model_runner.cc
    PRIV_REQUIRES spi_flash
    INCLUDE_DIRS ""
    PRIV_REQUIRES esp_timer nvs_flash bt)
