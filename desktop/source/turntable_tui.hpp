#pragma once

#include "ftxui/component/component.hpp"  // for Renderer, CatchEvent, Horizontal, Menu, Tab
#include "ftxui/component/component_base.hpp"      // for ComponentBase
#include "ftxui/component/event.hpp"               // for Event
#include "ftxui/component/mouse.hpp"               // for Mouse
#include "ftxui/component/screen_interactive.hpp"  // for ScreenInteractive
#include "ftxui/dom/canvas.hpp"                    // for Canvas
#include "ftxui/screen/color.hpp"  // for Color, Color::Red, Color::Blue, Color::Green, ftxui



auto temp() {
    std::vector<std::string> tab_values{
      "Azimuth",
      "Frequency Responce",
      "Phase",
      "THD",
      "Tracking Ablity",
      "Exit"
  };
  int tab_selected = 0;
  auto tab_toggle = ftxui::Toggle(&tab_values, &tab_selected);
 
  std::vector<std::string> tab_1_entries{
      "Forest",
      "Water",
      "I don't know",
  };
  int tab_1_selected = 0;
 
  std::vector<std::string> tab_2_entries{
      "Hello",
      "Hi",
      "Hay",
  };
  int tab_2_selected = 0;
 
  std::vector<std::string> tab_3_entries{
      "Table",
      "Nothing",
      "Is",
      "Empty",
  };
  int tab_3_selected = 0;
  auto tab_container = ftxui::Container::Tab(
      {
          ftxui::Radiobox(&tab_1_entries, &tab_1_selected),
          ftxui::Radiobox(&tab_2_entries, &tab_2_selected),
          ftxui::Radiobox(&tab_3_entries, &tab_3_selected),
      },
      &tab_selected);
 
  auto container = ftxui::Container::Vertical({
      tab_toggle,
      tab_container,
  });
 
  auto renderer = ftxui::Renderer(container, [&] {
    return ftxui::vbox({
               tab_toggle->Render(),
               ftxui::separator(),
               tab_container->Render(),
           }) |
           ftxui::border;
  });
 
  auto screen = ftxui::ScreenInteractive::TerminalOutput();
  screen.Loop(renderer);
}
