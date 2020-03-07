// Copyright (c) 2019 aNoken
// Arduino IDE compile code
//arduino-esp ver 1.04

#include "driver/spi_master.h"
#include "driver/spi_slave.h"
#include <Arduino.h>
#include <SPI.h>

static const uint32_t TRANS_SIZE = 1024;  //バッファのサイズ
uint8_t* spi_slave_tx_buf;          //バッファ格納先
uint8_t* spi_slave_rx_buf;

spi_slave_transaction_t spi_slave_trans;    //SPIスレーブ
spi_slave_interface_config_t spi_slave_cfg;
spi_bus_config_t spi_slave_bus;

static const uint8_t SPI_SLAVE_CS = 5;    // SPIのIO設定
static const uint8_t SPI_SLAVE_CLK = 18;
static const uint8_t SPI_SLAVE_MOSI = 14;
static const uint8_t SPI_SLAVE_MISO = 23;

void spi_buf_init();
void spi_slave_init();
void spi_slave_tans_done(spi_slave_transaction_t* trans);

void print_buf( uint8_t* buf, uint32_t len) {
  for (uint32_t i = 0; i < len; i++) {
    Serial.printf("%02X ", buf[i]);
  }
  Serial.println();
}

void setup() {
  Serial.begin(115200);
  spi_buf_init();
  spi_slave_init();
}

void loop() {
  // スレーブの送信準備
  spi_slave_queue_trans(VSPI_HOST, &spi_slave_trans, portMAX_DELAY);
  delay(10);
}

// SPI 通信バッファの初期化
void spi_buf_init() {
  spi_slave_tx_buf = (uint8_t*)heap_caps_malloc(TRANS_SIZE, MALLOC_CAP_DMA);
  spi_slave_rx_buf = (uint8_t*)heap_caps_malloc(TRANS_SIZE, MALLOC_CAP_DMA);
  for (uint32_t i = 0; i < TRANS_SIZE; i++) {
    spi_slave_tx_buf[i] = (0xFF - i) & 0xFF;
  }
  memset(spi_slave_rx_buf, 0, TRANS_SIZE);
}

// SPIスレーブ の初期化
void spi_slave_init() {
  spi_slave_trans.length = 8 * TRANS_SIZE;
  spi_slave_trans.rx_buffer = spi_slave_rx_buf;
  spi_slave_trans.tx_buffer = spi_slave_tx_buf;

  spi_slave_cfg.spics_io_num = SPI_SLAVE_CS;
  spi_slave_cfg.flags = 0;
  spi_slave_cfg.queue_size = 1;
  spi_slave_cfg.mode = SPI_MODE0;

  spi_slave_cfg.post_setup_cb = NULL;
  spi_slave_cfg.post_trans_cb = spi_slave_tans_done;

  spi_slave_bus.sclk_io_num = SPI_SLAVE_CLK;
  spi_slave_bus.mosi_io_num = SPI_SLAVE_MOSI;
  spi_slave_bus.miso_io_num = SPI_SLAVE_MISO;
  spi_slave_bus.max_transfer_sz = 8192;

  spi_slave_initialize(VSPI_HOST, &spi_slave_bus, &spi_slave_cfg, 1);

}

// スレーブの通信完了後に呼ばれるコールバック
void spi_slave_tans_done(spi_slave_transaction_t* trans) {
  Serial.print("SPI Slave RX:");
  print_buf( spi_slave_rx_buf, trans->trans_len / 8);
  Serial.print("SPI Slave TX:");
  print_buf( spi_slave_tx_buf, trans->trans_len / 8);

}
