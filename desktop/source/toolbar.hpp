#pragma once
#include "app_state.hpp"
#include "imgui.h"

static bool MainMenuBar(GuiState& gui_state)
{
  bool exit_app = false;
  if (ImGui::BeginMainMenuBar()) {
    if (ImGui::BeginMenu("File")) {
      if (ImGui::MenuItem("Save Results", "Ctrl+S")) {
      }

      if (ImGui::MenuItem("Settings", "Ctrl+.")) {
      }

      ImGui::Separator();
      if (ImGui::MenuItem("Quit", "Alt+F4")) {
        exit_app = true;
      }

      ImGui::EndMenu();
    }
    if (ImGui::BeginMenu("Tools")) {
      if (ImGui::MenuItem("Azimuth")) {
        gui_state.azimuth_window = true;
      }

      if (ImGui::MenuItem("THD")) {
        gui_state.thd_window = true;
      }

      if (ImGui::MenuItem("Frequency Response")) {
        gui_state.freq_response = true;
      }

      ImGui::EndMenu();
    }

    if (ImGui::BeginMenu("Run")) {
      if (ImGui::MenuItem("Azimuth")) {
      }
      if (ImGui::MenuItem("THD")) {
      }
      if (ImGui::MenuItem("Frequency Response")) {
      }
      if (ImGui::MenuItem("All")) {
      }
      ImGui::EndMenu();
    }

    ImGui::EndMainMenuBar();
  }
  return exit_app;
}