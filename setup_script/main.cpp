#include <iostream>
#include <string>
#include <vector>
#include <filesystem>
#include <fstream>
#include <regex>
#include <map>
#include <ctime>
#include <sstream>
#include <algorithm>
#include <iomanip>

namespace fs = std::filesystem;

// Global flags
bool DEBUG = false;
bool VERBOSE = false;

// Enums for navigation
enum class StepResult {
    NEXT,
    BACK,
    CANCEL
};

// Utils class
class Utils {
public:
    static std::string slugify(const std::string& name) {
        std::string result = name;
        std::regex invalid_chars("[^a-zA-Z0-9_-]");
        result = std::regex_replace(result, invalid_chars, "_");
        return result;
    }

    static std::string current_date() {
        auto t = std::time(nullptr);
        auto tm = *std::localtime(&t);
        std::ostringstream oss;
        oss << std::put_time(&tm, "%m/%d/%Y");
        return oss.str();
    }
};

// Prompter class
class Prompter {
public:
    static void clear_screen() {
#ifdef _WIN32
        std::system("cls");
#else
        std::system("clear");
#endif
    }

    static std::string get_input(const std::string& prompt_text, const std::string& default_val = "") {
        std::string input;
        std::cout << prompt_text;
        if (!default_val.empty()) {
            std::cout << " (default: " << default_val << ")";
        }
        std::cout << " > ";
        std::getline(std::cin, input);
        if (input.empty()) {
            return default_val;
        }
        return input;
    }

    static StepResult numbered_prompt(const std::string& title, const std::vector<std::string>& options, std::string& selection) {
        while (true) {
            std::cout << "\n" << title << "\n";
            for (size_t i = 0; i < options.size(); ++i) {
                std::cout << " " << (i + 1) << ". " << options[i] << "\n";
            }
            std::cout << "Select an option (or 'b' to back, 'q' to quit) > ";
            
            std::string input;
            std::getline(std::cin, input);

            if (input == "b" || input == "B") return StepResult::BACK;
            if (input == "q" || input == "Q") return StepResult::CANCEL;

            try {
                int choice = std::stoi(input);
                if (choice >= 1 && choice <= static_cast<int>(options.size())) {
                    selection = options[choice - 1];
                    return StepResult::NEXT;
                }
            } catch (...) {}
            
            std::cout << "Invalid selection. Try again.\n";
        }
    }
};

// Configuration structure
struct Config {
    std::string category;
    std::string project_name;
    std::string author;
    std::string difficulty;
    std::string tier;
    std::string level;
    std::string type;
    std::map<std::string, std::string> env;
};

// JSON Parser (Simple/Naive for defaults.json)
struct EnvSetting {
    std::string prompt;
    std::string default_val;
    bool required;
};

class DefaultLoader {
public:
    static std::map<std::string, EnvSetting> load_defaults(const std::string& path) {
        std::map<std::string, EnvSetting> settings;
        std::ifstream file(path);
        if (!file.is_open()) {
            std::cerr << "Could not open defaults.json at " << path << "\n";
            return settings;
        }

        std::stringstream buffer;
        buffer << file.rdbuf();
        std::string content = buffer.str();

        parse_content(content, settings);
        
        return settings;
    }

private:
    static void parse_content(const std::string& content, std::map<std::string, EnvSetting>& settings) {
        std::regex key_regex("\"([A-Z_]+)\"\\s*:\\s*\\{");
        std::smatch key_match;
        
        std::string::const_iterator search_start(content.cbegin());
        while (std::regex_search(search_start, content.cend(), key_match, key_regex)) {
            std::string key = key_match[1];
            size_t block_start = key_match.position() + key_match.length();
            size_t block_end = content.find('}', block_start);
            
            if (block_end != std::string::npos) {
                std::string block = content.substr(block_start, block_end - block_start);
                settings[key] = parse_setting_block(block);
            }
            
            search_start = content.cbegin() + block_end;
        }
    }

    static EnvSetting parse_setting_block(const std::string& block) {
        EnvSetting setting;
        std::regex prompt_re("\"prompt\"\\s*:\\s*\"([^\"]+)\"");
        std::regex default_re("\"default\"\\s*:\\s*\"([^\"]+)\"");
        std::regex required_re("\"required\"\\s*:\\s*(true|false)");
        
        std::smatch m;
        if (std::regex_search(block, m, prompt_re)) setting.prompt = m[1];
        if (std::regex_search(block, m, default_re)) setting.default_val = m[1];
        if (std::regex_search(block, m, required_re)) setting.required = (m[1] == "true");
        return setting;
    }
};

class Builder {
public:
    static void build_project(const Config& config) {
        fs::path base_dir = fs::current_path();
        fs::path template_dir = base_dir / "setup_script" / "TEMPLATE";
        fs::path project_dir = determine_project_dir(config, base_dir);

        if (fs::exists(project_dir)) {
            std::cerr << "Error: The project directory '" << project_dir.string() << "' already exists.\n";
            return;
        }

        copy_template(template_dir, project_dir);
        configure_writeup(config, project_dir);
        create_env_files(config, project_dir);
        
        std::cout << "Project created successfully at " << project_dir.string() << "\n";
    }

private:
    static fs::path determine_project_dir(const Config& config, const fs::path& base_dir) {
        std::string category_name = config.category;
        if (category_name == "Challenge") category_name = "Challenges";
        else if (category_name == "Machine") category_name = "Machines";
        else if (category_name == "Sherlock") category_name = "Sherlocks";
        
        fs::path category_dir = base_dir / category_name;
        fs::create_directories(category_dir);

        if (config.category == "Academy") {
            return category_dir / config.tier / config.level / config.type / Utils::slugify(config.project_name);
        } else {
            return category_dir / Utils::slugify(config.project_name);
        }
    }

    static void copy_template(const fs::path& template_dir, const fs::path& project_dir) {
        try {
            fs::copy(template_dir, project_dir, fs::copy_options::recursive);
        } catch (const fs::filesystem_error& e) {
            std::cerr << "Error copying template: " << e.what() << "\n";
        }
    }

    static void configure_writeup(const Config& config, const fs::path& project_dir) {
        fs::path writeup_path = project_dir / "writeup" / "WRITEUP.MD";
        if (!fs::exists(writeup_path)) return;

        std::ifstream in(writeup_path);
        std::stringstream buffer;
        buffer << in.rdbuf();
        std::string content = buffer.str();
        in.close();

        auto replace_all = [](std::string& str, const std::string& from, const std::string& to) {
            size_t start_pos = 0;
            while((start_pos = str.find(from, start_pos)) != std::string::npos) {
                str.replace(start_pos, from.length(), to);
                start_pos += to.length();
            }
        };

        replace_all(content, "[Challenge/Box Name]", config.project_name);
        replace_all(content, "[Created By]", config.author);
        replace_all(content, "[Difficulty Level]", config.difficulty);
        replace_all(content, "[2/17/2025]", Utils::current_date());

        std::ofstream out(writeup_path);
        out << content;
    }

    static void create_env_files(const Config& config, const fs::path& project_dir) {
        // Create vars.bash
        fs::path vars_bash_path = project_dir / "writeup" / "vars.bash";
        std::ofstream vars_file(vars_bash_path);
        for (const auto& pair : config.env) {
            vars_file << "export " << pair.first << "=" << pair.second << "\n";
        }

        // Create .env
        fs::path env_path = project_dir / ".env";
        std::ofstream env_file(env_path);
        for (const auto& pair : config.env) {
            env_file << pair.first << "=" << pair.second << "\n";
        }
    }
};

class FileManager {
public:
    static void update_readme(const Config& config) {
        fs::path readme_path = fs::current_path() / "README.md";
        if (!fs::exists(readme_path)) return;

        std::vector<std::string> lines = read_lines(readme_path);
        bool updated = insert_project_link(lines, config);

        if (updated) {
            write_lines(readme_path, lines);
        }
    }

private:
    static std::vector<std::string> read_lines(const fs::path& path) {
        std::ifstream in(path);
        std::vector<std::string> lines;
        std::string line;
        while (std::getline(in, line)) {
            lines.push_back(line);
        }
        return lines;
    }

    static void write_lines(const fs::path& path, const std::vector<std::string>& lines) {
        std::ofstream out(path);
        for (const auto& l : lines) {
            out << l << "\n";
        }
    }

    static bool insert_project_link(std::vector<std::string>& lines, const Config& config) {
        std::string category_header = "## " + config.category;
        std::string lower_header = category_header;
        std::transform(lower_header.begin(), lower_header.end(), lower_header.begin(), ::tolower);

        bool section_found = false;
        for (auto it = lines.begin(); it != lines.end(); ++it) {
            std::string current_line = *it;
            std::transform(current_line.begin(), current_line.end(), current_line.begin(), ::tolower);
            
            if (current_line.find(lower_header) != std::string::npos) {
                section_found = true;
                std::string link = "- [" + config.project_name + "](" + config.category + "/" + config.project_name + "/)";
                lines.insert(it + 1, link);
                return true;
            }
        }

        if (!section_found) {
            lines.push_back("");
            lines.push_back("## " + config.category);
            lines.push_back("- [" + config.project_name + "](" + config.category + "/" + config.project_name + "/)");
            return true;
        }
        return false;
    }
};

void display_status(const Config& config, const std::string& current_step, int step_num, int total_steps) {
    Prompter::clear_screen();
    std::cout << "==============================\n";
    std::cout << " Current Configuration Status\n";
    std::cout << "==============================\n";
    std::cout << "Category: " << (config.category.empty() ? "[Not set]" : config.category) << "\n";
    std::cout << "Project Name: " << (config.project_name.empty() ? "[Not set]" : config.project_name) << "\n";
    if (!config.tier.empty()) std::cout << "Tier: " << config.tier << "\n";
    if (!config.level.empty()) std::cout << "Level: " << config.level << "\n";
    if (!config.type.empty()) std::cout << "Type: " << config.type << "\n";
    if (!config.difficulty.empty()) std::cout << "Difficulty: " << config.difficulty << "\n";
    if (!config.author.empty()) std::cout << "Author: " << config.author << "\n";
    std::cout << "==============================\n";
    std::cout << " Step " << step_num << " of " << total_steps << ": " << current_step << "\n";
    std::cout << "==============================\n";
}

// State Handlers
StepResult handle_category(Config& config) {
    display_status(config, "Category", 1, 5);
    return Prompter::numbered_prompt("Select the category", {"Challenge", "Machine", "Sherlock", "Academy"}, config.category);
}

StepResult handle_project_name(Config& config) {
    display_status(config, "Project Name", 2, 5);
    std::cout << "Enter the Project/Module name (or 'b' to back, 'q' to quit) > ";
    std::string input;
    std::getline(std::cin, input);
    if (input == "q" || input == "Q") return StepResult::CANCEL;
    if (input == "b" || input == "B") return StepResult::BACK;
    if (input.empty()) return StepResult::BACK; // Or just stay? Original code continued if empty but didn't set. Let's assume user must enter something or loop.
    // Actually original code: if (input.empty()) continue; -> So it loops.
    // Here we can just recurse or return a special status, but let's just loop inside.
    if (input.empty()) return handle_project_name(config); 
    
    config.project_name = input;
    return StepResult::NEXT;
}

StepResult handle_academy_details(Config& config) {
    std::vector<std::pair<std::string, std::vector<std::string>>> academy_steps = {
        {"Tier", {"Tier 0", "Tier I", "Tier II", "Tier III", "Tier IV"}},
        {"Level", {"Fundamental", "Easy", "Medium", "Hard"}},
        {"Type", {"Offensive", "Defensive", "Purple", "General"}},
        {"Difficulty", {"Informational", "Easy", "Medium", "Hard"}}
    };
    
    for (auto& step : academy_steps) {
        std::string val;
        StepResult res = Prompter::numbered_prompt("Select " + step.first, step.second, val);
        if (res == StepResult::CANCEL) return StepResult::CANCEL;
        if (res == StepResult::BACK) return StepResult::BACK;
        
        if (step.first == "Tier") config.tier = val;
        else if (step.first == "Level") config.level = val;
        else if (step.first == "Type") config.type = val;
        else if (step.first == "Difficulty") config.difficulty = val;
    }
    return StepResult::NEXT;
}

StepResult handle_standard_details(Config& config) {
    StepResult res = Prompter::numbered_prompt("Select Difficulty", {"Easy", "Medium", "Hard", "Insane"}, config.difficulty);
    if (res == StepResult::CANCEL) return StepResult::CANCEL;
    if (res == StepResult::BACK) return StepResult::BACK;
    
    std::cout << "Enter the author name (or 'b' to back) > ";
    std::string auth;
    std::getline(std::cin, auth);
    if (auth == "b" || auth == "B") return StepResult::BACK;
    config.author = auth;
    return StepResult::NEXT;
}

StepResult handle_details(Config& config) {
    display_status(config, "Details", 3, 5);
    if (config.category == "Academy") {
        return handle_academy_details(config);
    } else {
        return handle_standard_details(config);
    }
}

StepResult handle_env_defaults(Config& config) {
    display_status(config, "Environment Defaults", 4, 5);
    fs::path defaults_path = fs::current_path() / "setup_script" / "defaults.json";
    auto defaults = DefaultLoader::load_defaults(defaults_path.string());
    
    for (const auto& pair : defaults) {
        std::string key = pair.first;
        EnvSetting setting = pair.second;
        
        std::string val = Prompter::get_input(setting.prompt, setting.default_val);
        config.env[key] = val;
    }
    return StepResult::NEXT;
}

int main(int argc, char* argv[]) {
    if (argc > 1) {
        std::string arg1 = argv[1];
        if (arg1 == "--debug") DEBUG = true;
        if (arg1 == "--verbose") VERBOSE = true;
    }

    Config config;
    int state = 0;
    
    while (true) {
        StepResult res = StepResult::NEXT;
        
        switch (state) {
            case 0: // Category
                res = handle_category(config);
                break;
            case 1: // Project Name
                res = handle_project_name(config);
                break;
            case 2: // Details
                res = handle_details(config);
                break;
            case 3: // Env Defaults
                res = handle_env_defaults(config);
                break;
            case 4: // Build
                Builder::build_project(config);
                FileManager::update_readme(config);
                return 0;
        }

        if (res == StepResult::CANCEL) return 0;
        if (res == StepResult::BACK) {
            if (state > 0) state--;
        } else if (res == StepResult::NEXT) {
            state++;
        }
    }

    return 0;
}
