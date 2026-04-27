/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2026 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include <string.h>
#include <stdio.h> // FOR UART CAN REMOVE FOR BLUETOOTH
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
SPI_HandleTypeDef hspi1;

/* USER CODE BEGIN PV */
DMA_HandleTypeDef hdma_spi1_rx;
DMA_HandleTypeDef hdma_spi1_tx;

UART_HandleTypeDef huart1; // this is used for reading data (not to be used with bluetooth)

/* USER CODE BEGIN PV */


/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
void PeriphCommonClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_DMA_Init(void);
static void MX_SPI1_Init(void);
static void MX_USART1_UART_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* Configure the peripherals common clocks */
  PeriphCommonClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_DMA_Init();
  MX_SPI1_Init();
  MX_USART1_UART_Init(); // MAKE SURE TO REMOVE FOR BLUETOOTH
  /* USER CODE BEGIN 2 */

  // ===== RESET =====
  HAL_GPIO_WritePin(ADS_RESET_GPIO_Port, ADS_RESET_Pin, GPIO_PIN_RESET);
  HAL_Delay(10);
  HAL_GPIO_WritePin(ADS_RESET_GPIO_Port, ADS_RESET_Pin, GPIO_PIN_SET);
  HAL_Delay(10);

  HAL_GPIO_WritePin(ADS_START_GPIO_Port, ADS_START_Pin, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_SET);
  HAL_Delay(1);

  // ===== SDATAC (device powers up in RDATAC, must exit before writing registers) =====
  uint8_t cmd_sdatac = 0x11;
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_RESET);
  HAL_SPI_Transmit(&hspi1, &cmd_sdatac, 1, HAL_MAX_DELAY);
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_SET);
  HAL_Delay(1);

  // ===== Read device ID (expect 0x3E for ADS1299) =====
  uint8_t rreg_tx[3] = {0x20, 0x00, 0x00};
  uint8_t rreg_rx[3] = {0};
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_RESET);
  HAL_SPI_TransmitReceive(&hspi1, rreg_tx, rreg_rx, 3, HAL_MAX_DELAY);
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_SET);
  volatile uint8_t device_id = rreg_rx[2];
  HAL_Delay(1);

  // ===== CONFIG1: 0x96 = 1001 0110
  // Bit7=1(reserved), DAISY_EN=0, CLK_EN=0, bits4:3=10(reserved), DR=110 => 250 SPS
  // 250 SPS is ideal for EEG (1-50 Hz bandwidth) =====
  uint8_t cfg1_write[3] = {0x41, 0x00, 0x96};
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_RESET);
  HAL_SPI_Transmit(&hspi1, cfg1_write, 3, HAL_MAX_DELAY);
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_SET);
  HAL_Delay(1);

  // ===== CONFIG2: 0xC0 = internal test signals OFF, no calibration signal =====
  uint8_t cfg2_write[3] = {0x42, 0x00, 0xC0};
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_RESET);
  HAL_SPI_Transmit(&hspi1, cfg2_write, 3, HAL_MAX_DELAY);
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_SET);
  HAL_Delay(1);

  // ===== CONFIG3: 0xEC = 1110 1100
  // PD_REFBUF=1 (enable internal ref), reserved=11,
  // BIAS_MEAS=0, BIASREF_INT=1 (internal midsupply ref for bias),
  // PD_BIAS=1 (bias amp ON), BIAS_LOFF_SENS=0, BIAS_STAT=0 =====
  uint8_t cfg3_write[3] = {0x43, 0x00, 0xEC};
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_RESET);
  HAL_SPI_Transmit(&hspi1, cfg3_write, 3, HAL_MAX_DELAY);
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_SET);
  HAL_Delay(150); // MUST wait >150ms for internal reference to settle

  // ===== CH1SET: 0x60 = gain=24 (110), SRB2=0, MUX=000 (normal electrode input)
  // Gain 24 gives best noise: ~0.14 uVPP at 250 SPS per datasheet Table 4 =====
  uint8_t ch1set_write[3] = {0x45, 0x00, 0x20};
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_RESET);
  HAL_SPI_Transmit(&hspi1, ch1set_write, 3, HAL_MAX_DELAY);
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_SET);
  HAL_Delay(1);

  // ===== Power down unused channels 2-8 with input shorted (MUX=001) =====
  // PDn=1, GAIN=110, SRB2=0, MUX=001 => 0xE1
  // This reduces noise coupling from floating inputs
  uint8_t ch_powerdown[3] = {0x46, 0x06, 0xE1}; // start at CH2SET (0x06), write 7 registers
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_RESET);
  HAL_SPI_Transmit(&hspi1, ch_powerdown, 1, HAL_MAX_DELAY);  // send WREG command byte
  uint8_t ch_powerdown_cmd = 0x06;  // 000n nnnn: write 7 registers (n=6)
  HAL_SPI_Transmit(&hspi1, &ch_powerdown_cmd, 1, HAL_MAX_DELAY);
  uint8_t ch_val = 0xE1;
  for (int i = 0; i < 7; i++) {
      HAL_SPI_Transmit(&hspi1, &ch_val, 1, HAL_MAX_DELAY);
  }
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_SET);
  HAL_Delay(1);

  // ===== BIAS_SENSP / BIAS_SENSN: route CH1 into bias drive =====
  // This creates common-mode feedback to stabilize electrode voltage within ADC range
  // Critical for real EEG electrodes on body
  uint8_t bias_sensp[3] = {0x4D, 0x00, 0x01}; // BIASP1 = 1 (CH1 positive into bias)
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_RESET);
  HAL_SPI_Transmit(&hspi1, bias_sensp, 3, HAL_MAX_DELAY);
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_SET);
  HAL_Delay(1);

  uint8_t bias_sensn[3] = {0x4E, 0x00, 0x01}; // BIASN1 = 1 (CH1 negative into bias)
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_RESET);
  HAL_SPI_Transmit(&hspi1, bias_sensn, 3, HAL_MAX_DELAY);
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_SET);
  HAL_Delay(1);

  // ===== RDATAC =====
  uint8_t cmd_rdatac = 0x10;
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_RESET);
  HAL_SPI_Transmit(&hspi1, &cmd_rdatac, 1, HAL_MAX_DELAY);
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_SET);
  HAL_Delay(1);

  // ===== Raise START to begin conversions =====
  HAL_GPIO_WritePin(ADS_START_GPIO_Port, ADS_START_Pin, GPIO_PIN_SET);
  HAL_Delay(10); // wait for filter to settle (tSETTLE = 32777 tCLK @ 250SPS ~ 16ms)

  uint8_t frame[27];
  uint8_t dummy_tx[27] = {0};
  int32_t dc_estimate = 0;
  int32_t ch1_filtered = 0;
  uint16_t warmup_samples = 0;
  uint8_t dc_initialized = 0;
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {


    /* USER CODE END WHILE */
	  // Wait for DRDY LOW
	     while (HAL_GPIO_ReadPin(ADS_DRDY_GPIO_Port, ADS_DRDY_Pin) == GPIO_PIN_SET);

	     HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_RESET);

	     HAL_SPI_TransmitReceive(&hspi1, dummy_tx, frame, 27, HAL_MAX_DELAY);

	     HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_SET);

	     int32_t ch1 = ((int32_t)frame[3] << 16) | ((int32_t)frame[4] << 8) | (int32_t)frame[5];

	     if (ch1 & 0x00800000)
	         ch1 |= 0xFF000000;

	     // Simple IIR DC removal (high pass)
	     if(!dc_initialized){
	    	 dc_estimate = ch1 << 8;
	    	 dc_initialized = 1;
	     }
	     dc_estimate = dc_estimate - (dc_estimate >> 8) + (ch1 >> 8);
	     ch1_filtered = ch1 - dc_estimate;

	     if (warmup_samples < 500){
	    	 warmup_samples++;
	    	 continue;
	     }

	     char msg[32];
	     sprintf(msg, "%ld\r\n", (long)ch1_filtered);
	     HAL_UART_Transmit(&huart1, (uint8_t*)msg, strlen(msg), HAL_MAX_DELAY);



    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI|RCC_OSCILLATORTYPE_MSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.MSIState = RCC_MSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.MSICalibrationValue = RCC_MSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.MSIClockRange = RCC_MSIRANGE_6;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Configure the SYSCLKSource, HCLK, PCLK1 and PCLK2 clocks dividers
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK4|RCC_CLOCKTYPE_HCLK2
                              |RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_MSI;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.AHBCLK2Divider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.AHBCLK4Divider = RCC_SYSCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief Peripherals Common Clock Configuration
  * @retval None
  */
void PeriphCommonClock_Config(void)
{
  RCC_PeriphCLKInitTypeDef PeriphClkInitStruct = {0};

  /** Initializes the peripherals clock
  */
  PeriphClkInitStruct.PeriphClockSelection = RCC_PERIPHCLK_SMPS;
  PeriphClkInitStruct.SmpsClockSelection = RCC_SMPSCLKSOURCE_HSI;
  PeriphClkInitStruct.SmpsDivSelection = RCC_SMPSCLKDIV_RANGE1;

  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN Smps */

  /* USER CODE END Smps */
}

/**
  * @brief SPI1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_SPI1_Init(void)
{

  /* USER CODE BEGIN SPI1_Init 0 */

  /* USER CODE END SPI1_Init 0 */

  /* USER CODE BEGIN SPI1_Init 1 */

  /* USER CODE END SPI1_Init 1 */
  /* SPI1 parameter configuration*/
  hspi1.Instance = SPI1;
  hspi1.Init.Mode = SPI_MODE_MASTER;
  hspi1.Init.Direction = SPI_DIRECTION_2LINES;
  hspi1.Init.DataSize = SPI_DATASIZE_8BIT;
  hspi1.Init.CLKPolarity = SPI_POLARITY_LOW;
  hspi1.Init.CLKPhase = SPI_PHASE_2EDGE;
  hspi1.Init.NSS = SPI_NSS_SOFT;
  hspi1.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_4;
  hspi1.Init.FirstBit = SPI_FIRSTBIT_MSB;
  hspi1.Init.TIMode = SPI_TIMODE_DISABLE;
  hspi1.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
  hspi1.Init.CRCPolynomial = 7;
  hspi1.Init.CRCLength = SPI_CRC_LENGTH_DATASIZE;
  hspi1.Init.NSSPMode = SPI_NSS_PULSE_DISABLE;
  if (HAL_SPI_Init(&hspi1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN SPI1_Init 2 */

  /* USER CODE END SPI1_Init 2 */

}

/**
  * @brief USART1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART1_UART_Init(void)
{

  /* USER CODE BEGIN USART1_Init 0 */

  /* USER CODE END USART1_Init 0 */

  /* USER CODE BEGIN USART1_Init 1 */

  /* USER CODE END USART1_Init 1 */
  huart1.Instance = USART1;
  huart1.Init.BaudRate = 115200;
  huart1.Init.WordLength = UART_WORDLENGTH_8B;
  huart1.Init.StopBits = UART_STOPBITS_1;
  huart1.Init.Parity = UART_PARITY_NONE;
  huart1.Init.Mode = UART_MODE_TX_RX;
  huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart1.Init.OverSampling = UART_OVERSAMPLING_16;
  huart1.Init.OneBitSampling = UART_ONE_BIT_SAMPLE_DISABLE;
  huart1.Init.ClockPrescaler = UART_PRESCALER_DIV1;
  huart1.AdvancedInit.AdvFeatureInit = UART_ADVFEATURE_NO_INIT;
  if (HAL_UART_Init(&huart1) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_UARTEx_SetTxFifoThreshold(&huart1, UART_TXFIFO_THRESHOLD_1_8) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_UARTEx_SetRxFifoThreshold(&huart1, UART_RXFIFO_THRESHOLD_1_8) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_UARTEx_DisableFifoMode(&huart1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART1_Init 2 */

  /* USER CODE END USART1_Init 2 */

}

/**
  * Enable DMA controller clock
  */
static void MX_DMA_Init(void)
{

  /* DMA controller clock enable */
  __HAL_RCC_DMAMUX1_CLK_ENABLE();
  __HAL_RCC_DMA1_CLK_ENABLE();

  /* DMA interrupt init */
  /* DMA1_Channel1_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(DMA1_Channel1_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(DMA1_Channel1_IRQn);
  /* DMA1_Channel2_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(DMA1_Channel2_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(DMA1_Channel2_IRQn);

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};
  /* USER CODE BEGIN MX_GPIO_Init_1 */

  /* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(ADS_RESET_GPIO_Port, ADS_RESET_Pin, GPIO_PIN_SET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(ADS_START_GPIO_Port, ADS_START_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(ADS_CS_GPIO_Port, ADS_CS_Pin, GPIO_PIN_SET);

  /*Configure GPIO pin : ADS_DRDY_Pin */
  GPIO_InitStruct.Pin = ADS_DRDY_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(ADS_DRDY_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : ADS_RESET_Pin ADS_START_Pin */
  GPIO_InitStruct.Pin = ADS_RESET_Pin|ADS_START_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /*Configure GPIO pin : ADS_CS_Pin */
  GPIO_InitStruct.Pin = ADS_CS_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(ADS_CS_GPIO_Port, &GPIO_InitStruct);

  /* USER CODE BEGIN MX_GPIO_Init_2 */

  /* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */

// NOT TO BE USED WITH BLUETOOTH


int __io_putchar(int ch)
{
    HAL_UART_Transmit(&huart1, (uint8_t *)&ch, 1, HAL_MAX_DELAY);
    return ch;
}

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}
#ifdef USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
