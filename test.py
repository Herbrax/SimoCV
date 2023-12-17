import re
import json
# Helper Function
def replace_tagged_content(html_content, tag, new_content):
    pattern = f"<!--{tag}/-->(.*?)<!--{tag}\\\\-->"
    replacement = f"<!--{tag}/-->{new_content}<!--{tag}\\\\-->"
    return re.sub(pattern, replacement, html_content, flags=re.DOTALL)

def map_level_to_class(level):
    if level == "Advanced":
        return "skills__80"
    elif level == "Intermediate":
        return "skills__60"
    elif level == "Beginner":
        return "skills__20"
    else:
        return ""

# Generating sections
def generate_skills_section(skills_data):
    html_skills_section = '<section class="skills section" id="skills" data-id="skills">\n'
    html_skills_section += '    <h2 class="section__title">Skills</h2>\n'
    html_skills_section += '    <span class="section__subtitle">Technical Competence</span>\n'
    html_skills_section += '    <div class="skills__container container grid">\n'

    for category in skills_data:
        html_skills_section += f'        <div class="skills__area">\n'
        html_skills_section += f'            <h3 class="category-title">{category["category"]}</h3>\n'
        html_skills_section += '            <div class="skills__content skills__open">\n'
        html_skills_section += '                <div class="skills__list grid">\n'

        for skill in category['skills']:
            level_class = map_level_to_class(skill["level"])
            html_skills_section += '                    <div class="skills__data">\n'
            html_skills_section += f'                        <div class="skills__titles">\n'
            html_skills_section += f'                            <h3 class="skills__name">{skill["name"]}</h3>\n'
            html_skills_section += f'                            <span class="skills__number">{skill["level"]}</span>\n'
            html_skills_section += '                        </div>\n'
            html_skills_section += f'                        <div class="skills__bar">\n'
            html_skills_section += f'                            <span class="skills__percantage {level_class}"></span>\n'
            html_skills_section += '                        </div>\n'
            html_skills_section += '                    </div>\n'

        html_skills_section += '                </div>\n'
        html_skills_section += '            </div>\n'
        html_skills_section += '        </div>\n'

    html_skills_section += '    </div>\n'
    html_skills_section += '</section>\n'
    return html_skills_section
def generate_qualifications_section(education_data, work_experience_data):
    qualifications_html = '''
    <section class="qualification section" id="qualifications" data-id="qualifications">
        <h2 class="section__title">Qualifications</h2>
        <span class="section__subtitle">Academic and Professional Career</span>
        <div class="qualification__container container">
            <!-- Education Content -->
            <div class="qualification__content qualification__active" data-content="" id="education">
                <h3 class="category-title">Education</h3>
    '''

    # Generating Education Entries
    for index, edu in enumerate(education_data, start=1):
        last_attr = 'name="Last"' if index == len(education_data) else ''
        qualifications_html += f'''
            <div class="qualification__data" id="index{index}" {last_attr}>
                <!--A-->
                <div>
                    <span class="qualification__degree">{edu["degree"]}</span>
                    <h3 class="qualification__title">{edu["field"]}</h3>
                    <span class="qualification__subtitle">{edu["institution"]}</span>
                    <div class="qualification__calendar"><i class="uil uil-calendar-alt"></i>{edu["year"]}</div>
                    <span class="qualification__details">{edu["details"]}</span>
                </div>
                <!--B-->
            </div>
        '''

    qualifications_html += '''
        </div>
        <div class="qualification__vertical-line"></div>
        <!-- Work Content -->
        <div class="qualification__content qualification__active" data-content="" id="work">
            <h3 class="category-title">Work</h3>
    '''

    # Generating Work Experience Entries
    for index, work in enumerate(work_experience_data, start=1):
        last_attr = 'name="Last"' if index == len(work_experience_data) else ''
        qualifications_html += f'''
            <div class="qualification__data" id="index{index}" {last_attr}>
                <!--A-->
                <div>
                    <h3 class="qualification__title">{work["position"]}</h3>
                    <span class="qualification__subtitle">{work["company"]}</span>
                    <div class="qualification__calendar"><i class="uil uil-calendar-alt"></i>{work["years"]}</div>
                    <span class="qualification__details">{work["details"]}</span>
                </div>
                <!--B-->
            </div>
        '''

    qualifications_html += '''
            </div>
        </div>
    </section>
    '''
    # Replacing <!--A--> and <!--B--> based on odd or even index
    lines = qualifications_html.split('\n')
    for i, line in enumerate(lines):
        if '<div class="qualification__data" id="index' in line:
            index = int(line.split('id="index')[1].split('"')[0])
            is_last = 'name="Last"' in line
            # Replace <!--A--> for odd indices
            if index % 2 != 0:
                j = i + 1  # The next line after the div line
                while j < len(lines) and '<!--A-->' not in lines[j]:
                    j += 1
                if j < len(lines):
                    if is_last:
                        lines[j] = '<div class="ignore"></div><div class="even"><span class="qualification__rounder"></span></div>'
                    else: lines[j] = '<div class="ignore"></div><div class="even"><span class="qualification__rounder"></span><span class="qualification__line"></span></div>'
            # Replace <!--B--> for even indices
            else:
                j = i + 1  # The next line after the div line
                while j < len(lines) and '<!--B-->' not in lines[j]:
                    j += 1
                if j < len(lines):
                    if is_last:
                        lines[j] = '<div class="even"><span class="qualification__rounder"></span></div>'
                    else: lines[j] = '<div class="odd"><span class="qualification__rounder"></span><span class="qualification__line"></span></div>'
    qualifications_html = '\n'.join(lines)
    return qualifications_html
def generate_testimonials_section(testimonials_data):
    testimonials_html = '''
    <section class="testimonial section" id="testimonials" data-id="testimonials">
        <h2 class="section__title">References</h2>
        <span class="section__subtitle">Testimonials</span>
        <div class="testimonial__container container">
    '''

    for testimonial in testimonials_data:
        testimonials_html += f'''
            <div>
                <div class="testimonial__data">
                    <div class="testimonial__header">
                        <img src="{testimonial["image"]}" alt="" class="testimonial__img">
                        <div>
                            <h3 class="testimonial__name">{testimonial["name"]}</h3>
                            <span class="testimonial__client">{testimonial["role"]}</span>
                        </div>
                    </div>
                </div>
                <p class="testimonial__description">{testimonial["testimonial"]}</p>
            </div>
        '''

    testimonials_html += '''
        </div>
    </section>
    '''
    return testimonials_html

# Update basic HTML with data from JSON
def update_html_with_json_data(json_data, html_content):
    # Replace HomeTitle
    home_title = "<title>" + json_data['personalInfo']['surname'] + " " + json_data['personalInfo']['lastname'] + "'s Portal 👋" + "</title>"
    html_content = replace_tagged_content(html_content, "HomeTitle", home_title)

    # Replace SurnameTitle
    surname_title = f'Hi, I am {json_data["personalInfo"]["surname"]}.'
    html_content = replace_tagged_content(html_content, "SurnameTitle", surname_title)

    # Replace Title
    title = json_data['personalInfo']['title']
    html_content = replace_tagged_content(html_content, "Title", title)
    
    # Replace Name
    full_name = json_data['personalInfo']['surname'] + " " + json_data['personalInfo']['lastname']
    html_content = replace_tagged_content(html_content, "Name", full_name)

    # Replace Home Description
    home_description = json_data['home']['description']
    html_content = replace_tagged_content(html_content, "Home Description", home_description)

    # Replace About Description
    about_description = json_data['about']['description']
    html_content = replace_tagged_content(html_content, "About Description", about_description)

    # Replace Social Links
    html_content = replace_tagged_content(html_content, "Linkedin", f'<a href="{json_data["socialLinks"]["linkedin"]}" target="_blank" class="social-icon" id="linkedin-icon"><i class="uil uil-linkedin"></i></a>')
    html_content = replace_tagged_content(html_content, "Github", f'<a href="{json_data["socialLinks"]["github"]}" target="_blank" class="social-icon" id="github-icon"><i class="uil uil-github"></i></a>')
    html_content = replace_tagged_content(html_content, "Twitter", f'<a href="{json_data["socialLinks"]["twitter"]}" target="_blank" class="social-icon" id="twitter-icon"><i class="uil uil-twitter"></i></a>')
    html_content = replace_tagged_content(html_content, "Linkedin2", f'<a href="{json_data["socialLinks"]["linkedin"]}" target="_blank" class="home__social-icon"><i class="uil uil-linkedin-alt"></i></a>')
    html_content = replace_tagged_content(html_content, "Github2", f'<a href="{json_data["socialLinks"]["github"]}" target="_blank" class="home__social-icon"><i class="uil uil-github-alt"></i></a>')
    html_content = replace_tagged_content(html_content, "Linkedin Footer", f'<a href="{json_data["socialLinks"]["linkedin"]}" target="_blank" class="footer__social"><i class="uil uil-linkedin-alt"></i></a>')
    html_content = replace_tagged_content(html_content, "Github Footer", f'<a href="{json_data["socialLinks"]["github"]}" target="_blank" class="footer__social"><i class="uil uil-github-alt"></i></a>')

    # Replace Phone
    phone = json_data['personalInfo']['contact']['phone']
    html_content = replace_tagged_content(html_content, "Phone", phone)

    # Replace Email Contact
    email = f'<p><a class="contact__subtitle" href="mailto:{json_data["personalInfo"]["contact"]["email"]}">{json_data["personalInfo"]["contact"]["email"]}</a></p>'
    html_content = replace_tagged_content(html_content, "Email Contact", email)

    # Replace Location
    location = json_data['personalInfo']['contact']['location']
    html_content = replace_tagged_content(html_content, "Location", location)
    
    ############################ Sections : 
    sections = ""
    sections += generate_skills_section(json_data["skills"])
    sections += generate_qualifications_section(json_data["education"], json_data["workExperience"])
    sections += generate_testimonials_section(json_data["testimonials"])

    # Replace Sections
    html_content = replace_tagged_content(html_content, "AUTOGENERATED", sections)

    return html_content

# Fonction pour mettre à jour le fichier CSS avec les couleurs du mode sombre
def update_css_with_json_colors(json_data, css_input_path, css_output_path):
    # Charger les couleurs depuis le JSON
    light_colors = json_data["colors"]["light"]
    dark_colors = json_data["colors"]["dark"]

    # Lire le fichier CSS
    with open(css_input_path, 'r', encoding='utf-8') as file:
        css_content = file.read()

    # Mettre à jour les couleurs pour le mode clair
    light_mode_section = '/*<light mode>*/\n'
    for color_name, color_value in light_colors.items():
        light_mode_section += f'    --{color_name}: {color_value};\n'
    light_mode_section += '    /*</light mode>*/\n'

    # Mettre à jour les couleurs pour le mode sombre
    dark_mode_section = '/*<dark mode>*/\n'
    for color_name, color_value in dark_colors.items():
        dark_mode_section += f'    --{color_name}: {color_value};\n'
    dark_mode_section += '    /*</dark mode>*/\n'

    # Remplacer les sections dans le CSS
    css_content = re.sub(r'/\*<light mode>\*/.*?/\*</light mode>\*/', light_mode_section, css_content, flags=re.DOTALL)
    css_content = re.sub(r'/\*<dark mode>\*/.*?/\*</dark mode>\*/', dark_mode_section, css_content, flags=re.DOTALL)

    # Enregistrer les modifications dans le nouveau fichier CSS
    with open(css_output_path, 'w', encoding='utf-8') as file:
        file.write(css_content)

# Example usage
json_data = {
    # JSON data here
}

# Chemin vers le fichier CSS
css_input_path = 'assets/css/styles.css'
# Chemin vers le nouveau fichier CSS
css_output_path = 'assets/css/styles.css'

# Load JSON data
with open('data.json', 'r') as file:
    json_data = json.load(file)

# Load HTML content
with open('Input.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Update HTML content with JSON data
updated_html_content = update_html_with_json_data(json_data, html_content)
# Mise à jour du fichier CSS
update_css_with_json_colors(json_data, css_input_path, css_output_path)

# Save the updated HTML content
output_file_path = 'index.html'
with open(output_file_path, 'w', encoding='utf-8') as file:
    print("completed task")
    file.write(updated_html_content)
