#ifndef MAIN_H
#define MAIN_H

void gap_event_handler(esp_gap_ble_cb_event_t event, esp_ble_gap_cb_param_t *param);
void display_devices_task(void *param);

#endif // MAIN_H