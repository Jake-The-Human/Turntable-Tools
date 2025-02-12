#pragma once

#include <filesystem>
#include <map>
#include <string>
#include <unordered_map>

class MessageCatalog
{
public:
  ~MessageCatalog() = default;

  static MessageCatalog& getInstance() { return *instance; }

  static void newInstance()
  {
    if (instance == nullptr) {
      instance = new MessageCatalog();
      instance->set_lang("en");
    }
  }

  static void deleteInstance()
  {
    if (instance != nullptr) {
      delete instance;
    }
  }

  bool set_lang(const std::string& lang);
  const char* get_message(const std::string& message) const;
  auto get_available_languages() const
      -> const std::map<std::string, std::filesystem::path>&;

private:
  static MessageCatalog* instance;
  std::map<std::string, std::filesystem::path> available_languages;
  std::unordered_map<std::string, std::string> messages;

  MessageCatalog();

  MessageCatalog(const MessageCatalog&) = delete;
  MessageCatalog(MessageCatalog&&) = delete;

  MessageCatalog& operator=(const MessageCatalog&) = delete;
  MessageCatalog& operator=(MessageCatalog&&) = delete;
};
