#include <cmath>
#include <vector>

#include "frequency_response_window.hpp"

#include "imgui.h"
#include "implot.h"

void FrequencyResponseWindow::renderUI(
    bool& window_state,
    std::future<std::pair<FrequencyResponseResults, FrequencyResponseResults>>&
        fr_results,
    bool file_loaded)
{
  if (fr_results.valid()) {
    auto results = fr_results.get();
    auto size = results.first.size();

    freq_left.resize(size);
    magnitude_left.resize(size);
    phase_left.resize(size);

    size_t i = 0;
    for (const auto& [x, s] : results.first) {
      freq_left[i] = x;
      magnitude_left[i] = s.first;
      phase_left[i] = s.second;
      i++;
    }

    freq_right.resize(size);
    magnitude_right.resize(size);
    phase_right.resize(size);
    i = 0;
    for (const auto& [x, s] : results.second) {
      freq_right[i] = x;
      magnitude_right[i] = s.first;
      phase_right[i] = s.second;
      i++;
    }
  }

  ImGui::Begin("Frequency Response", &window_state);
  if (file_loaded) {
    static int item_selected_idx = 0;
    static const std::array<const char*, 3> items = {"Stereo", "Left", "Right"};
    if (ImGui::BeginCombo("Graph", items[item_selected_idx])) {
      for (int n = 0; n < items.size(); n++) {
        const bool is_selected = (item_selected_idx == n);
        if (ImGui::Selectable(items[n], is_selected))
          item_selected_idx = n;

        // Set the initial focus when opening the combo (scrolling +
        // keyboard navigation focus)
        if (is_selected)
          ImGui::SetItemDefaultFocus();
      }
      ImGui::EndCombo();
    }

    if (ImPlot::BeginSubplots(
            "Bode Plot", 2, 1, ImVec2(-1, -1), ImPlotSubplotFlags_LinkAllX))
    {
      if (ImPlot::BeginPlot("Frequency vs Magnitude")) {
        ImPlot::SetupAxes("Frequency (Hz)", "Magnitude (dB)", 0, 0);
        ImPlot::SetupAxisScale(ImAxis_X1, ImPlotScale_SymLog);
        ImPlot::SetupAxesLimits(0, 22000, -60, 20);
        if (item_selected_idx == 0 || item_selected_idx == 1) {
          ImPlot::PlotLine("Left",
                           freq_left.data(),
                           magnitude_left.data(),
                           freq_left.size());
        }
        if (item_selected_idx == 0 || item_selected_idx == 2) {
          ImPlot::PlotLine("Right",
                           freq_right.data(),
                           magnitude_right.data(),
                           freq_right.size());
        }
        ImPlot::EndPlot();
      }

      if (ImPlot::BeginPlot("Frequency vs Phase")) {
        ImPlot::SetupAxes("Frequency (Hz)", "Phase (degrees)", 0, 0);
        ImPlot::SetupAxisScale(ImAxis_X1, ImPlotScale_SymLog);
        ImPlot::SetupAxesLimits(0, 22000, -180, 180);
        if (item_selected_idx == 0 || item_selected_idx == 1) {
          ImPlot::PlotLine(
              "Left", freq_left.data(), phase_left.data(), freq_left.size());
        }
        if (item_selected_idx == 0 || item_selected_idx == 2) {
          ImPlot::PlotLine("Right",
                           freq_right.data(),
                           phase_right.data(),
                           freq_right.size());
        }
        ImPlot::EndPlot();
      }

      ImPlot::EndSubplots();
    }
  } else {
    ImGui::Text("No File loaded.");
  }
  ImGui::End();
}
