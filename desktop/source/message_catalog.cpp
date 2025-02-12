#include <filesystem>
#include <fstream>

#include "message_catalog.hpp"

MessageCatalog* MessageCatalog::instance = nullptr;

MessageCatalog::MessageCatalog()
{
  // Find available languages
  for (const auto& file : std::filesystem::directory_iterator {LANGUAGE_DIR}) {
    const auto& file_path = file.path();
    available_languages.insert({file_path.stem().c_str(), file_path});
  }
}

bool MessageCatalog::set_lang(const std::string& lang)
{
  std::fstream lang_file(available_languages.at(lang));
  if (!lang_file.is_open()) {
    return false;
  }
  std::string line;
  while (std::getline(lang_file, line)) {
    auto pos = line.find("=");
    if (pos != std::string::npos) {
      messages.insert({line.substr(0, pos), line.substr(pos + 1)});
    } else {
      // should print out some log or something
      return false;
    }
  }

  return true;
}

const char* MessageCatalog::get_message(const std::string& message) const
{
  return messages.count(message) ? messages.at(message).data()
                                 : "Message not found";
}

auto MessageCatalog::get_available_languages() const
    -> const std::map<std::string, std::filesystem::path>&
{
  return available_languages;
}
