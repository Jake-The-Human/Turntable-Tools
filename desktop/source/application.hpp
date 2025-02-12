#pragma once

#include "audio_window.hpp"
#include "azimuth_window.hpp"
#include "frequency_response_window.hpp"
#include "thd_window.hpp"

constexpr auto NUMBER_OF_TESTS = 3;

struct MyApp
{
  bool renderUI();
  void updateState();
  bool MainMenuBar();

  AudioWindow audio_window;
  AzimuthWindow azimuth_window;
  ThdWindow thd_window;
  FrequencyResponseWindow freq_window;

  bool analyzing_modal = false;
};
