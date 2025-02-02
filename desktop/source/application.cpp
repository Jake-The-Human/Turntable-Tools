#include <cmath>
#include <cstdio>

#include "application.hpp"

#include <imgui.h>
#include <implot.h>

namespace
{

void AzimuthWindow(MyApp::GuiState& gui_state)
{
  ImGui::Begin("Azimuth", &gui_state.azimuth_window, ImGuiWindowFlags_MenuBar);

  ImGui::End();
}

void ThdWindow(MyApp::GuiState& gui_state)
{
  ImGui::Begin("THD", &gui_state.thd_window, ImGuiWindowFlags_MenuBar);

  ImGui::End();
}

void FrequencyResponse(MyApp::GuiState& gui_state)
{
  ImGui::Begin(
      "Frequency Response", &gui_state.freq_response, ImGuiWindowFlags_MenuBar);

  ImGui::End();
}
}  // namespace

void file_menu_bar() {}

bool MyApp::renderUI(const ImGuiIO& io)
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
      gui_state.azimuth_window = ImGui::MenuItem("Azimuth");
      gui_state.thd_window = ImGui::MenuItem("THD");
      gui_state.freq_response = ImGui::MenuItem("Frequency Response");
      ImGui::EndMenu();
    }
    ImGui::EndMainMenuBar();
  }

  audio_window.renderUI();

  if (gui_state.azimuth_window) {
    AzimuthWindow(MyApp::gui_state);
  }

  if (gui_state.thd_window) {
    ThdWindow(gui_state);
  }

  if (gui_state.freq_response) {
    FrequencyResponse(gui_state);
  }

  // ImGui::CreateContext();
  // ImPlot::CreateContext();
  // ImPlot::ShowDemoWindow();
  // ImPlot::DestroyContext();
  // ImGui::DestroyContext();
  // ImGui::ShowDemoWindow();
  return exit_app;
}
