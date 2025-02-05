#include <algorithm>

#include "azimuth_window.hpp"

#include <imgui.h>

#include "tools/azimuth.hpp"

static void HelpMarker(const char* desc)
{
  ImGui::TextDisabled("(?)");
  if (ImGui::BeginItemTooltip()) {
    ImGui::PushTextWrapPos(ImGui::GetFontSize() * 35.0f);
    ImGui::TextUnformatted(desc);
    ImGui::PopTextWrapPos();
    ImGui::EndTooltip();
  }
}

void AzimuthWindow::renderUI(bool& window_state,
                             std::future<azimuth::Results>& azimuth_results,
                             bool file_loaded)
{
  ImGui::Begin("Azimuth", &window_state);

  if (azimuth_results.valid()) {
    results = azimuth_results.get();
  }

  if (file_loaded) {
    ImGui::InputInt("Test Tone (Hz)", &test_frequency, 100, 1000);
    test_frequency = std::clamp(test_frequency, 0, 22000);
    static const std::array<const char*, 2> combo_text = {"Left", "Right"};
    static int item_selected_idx = 0;
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
    ImGui::Separator();

    if (item_selected_idx == 0) {
      ImGui::Text("Left crosstalk: %fdB", results.crosstalk_signal_1);
    } else {
      ImGui::Text("Right crosstalk:  %fdB", results.crosstalk_signal_2);
    }
  } else {
    ImGui::Text("No File loaded.");
  }
  ImGui::End();
}
