#include "thd_window.hpp"

#include "imgui.h"

void ThdWindow::renderUI(bool& window_state,
                         std::future<std::pair<float, float>>& thd_results,
                         bool file_loaded)
{
  if (thd_results.valid()) {
    results = thd_results.get();
  }

  ImGui::Begin("THD", &window_state);
  if (file_loaded) {
    ImGui::Text("Left Channel: %.2f%%", results.first);
    ImGui::Text("Right Channel: %.2f%%", results.second);
  } else {
    ImGui::Text("No File loaded.");
  }
  ImGui::End();
}
