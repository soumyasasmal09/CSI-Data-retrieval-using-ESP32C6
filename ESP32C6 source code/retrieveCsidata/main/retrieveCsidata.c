#include "esp_wifi.h"
#include "esp_event.h"
#include "nvs_flash.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"

static const char* TAG = "CSI_APP";

void csi_callback(void* ctx, wifi_csi_info_t* csi_info) {
    ESP_LOGI(TAG, "CSI data received: len=%d, first_word=%d", csi_info->len, csi_info->buf[0]);
    for (int i = 0; i < csi_info->len; i++) {
        printf("%d ", csi_info->buf[i]);
    }
    printf("\n");
}

void app_main(void) {
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());

    esp_netif_create_default_wifi_sta();

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_start());

    wifi_config_t wifi_config = {
        .sta = {
            .ssid = "ssid",
            .password = "your password",
        },
    };
    ESP_ERROR_CHECK(esp_wifi_set_config(ESP_IF_WIFI_STA, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_connect());

    // Register CSI callback
    ESP_ERROR_CHECK(esp_wifi_set_csi_rx_cb(csi_callback, NULL));

    // Enable CSI collection
    ret = esp_wifi_set_csi(true);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to enable CSI: %s", esp_err_to_name(ret));
    }
    else {
        ESP_LOGI(TAG, "CSI collection enabled successfully");
    }

    ESP_LOGI(TAG, "Initialization complete, CSI collection started");
}
