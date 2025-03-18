#include <algorithm>
#include <array>

#include "azimuth_window.hpp"

#include <imgui.h>

#include "tools/azimuth.hpp"

void AzimuthWindow::renderUI(bool& window_state,
                             std::future<azimuth::Results>& azimuth_results,
                             bool file_loaded)
{
  ImGui::Begin("Azimuth", &window_state);

  if (azimuth_results.valid()) {
    results = azimuth_results.get();
  }

  if (file_loaded) {
    ImGui::BeginGroup();
    ImGui::InputInt("Test Tone (Hz)", &test_frequency, 100, 1000);
    if (ImGui::IsItemHovered(ImGuiHoveredFlags_Stationary)) {
      ImGui::SetTooltip("This is the frequency that your test record is playing.");
    }
    ImGui::EndGroup();

    test_frequency = std::clamp(test_frequency, 0, 22000);
    static const std::array<const char*, 2> combo_text = {"Left", "Right"};
    static int item_selected_idx = 0;
    ImGui::BeginGroup();
    if (ImGui::BeginCombo("Channel", combo_text[item_selected_idx])) {
      for (int n = 0; n < combo_text.size(); n++) {
        const bool is_selected = (item_selected_idx == n);
        if (ImGui::Selectable(combo_text[n], is_selected))
          item_selected_idx = n;

        // Set the initial focus when opening the combo (scrolling +
        // keyboard navigation focus)
        if (is_selected)
          ImGui::SetItemDefaultFocus();
      }
      ImGui::EndCombo();
    }
    if (ImGui::IsItemHovered(ImGuiHoveredFlags_Stationary)) {
      ImGui::SetTooltip("This is the channel that the test tone is playing on.");
    }
    ImGui::EndGroup();

    ImGui::Separator();

    ImGui::BeginGroup();
    if (item_selected_idx == 0) {
      ImGui::Text("Left crosstalk: %.3fdB", results.crosstalk_signal_1);
    } else {
      ImGui::Text("Right crosstalk:  %.3fdB", results.crosstalk_signal_2);
    }
    if (ImGui::IsItemHovered(ImGuiHoveredFlags_Stationary)) {
      ImGui::SetTooltip("This is how much of the other channel is audible. (lower is better)");
    }
    ImGui::EndGroup();

    ImGui::BeginGroup();
    ImGui::Text("Phase difference:  %.3f degrees", results.phase_diff);
    if (ImGui::IsItemHovered(ImGuiHoveredFlags_Stationary)) {
      ImGui::SetTooltip("This is the phase difference. This can be used if both tracks have the same test tone.\nIn that case, you want this to be as close to 0 as possible.");
    }
    ImGui::EndGroup();

  } else {
    ImGui::Text("No File loaded.");
  }
  ImGui::End();
}
