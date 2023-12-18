import re
import json

####### -- CSS Update -- #######
# Update CSS with color data from JSON
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
        print("completed task - CSS")
        file.write(css_content)
################################

####### -- HTML Update -- #######
    # Helper Function -- Replace content in custom comment tags <!--TAG/--><!--TAG\-->
def replace_tagged_content(html_content, tag, new_content):
    pattern = f"<!--{tag}/-->(.*?)<!--{tag}\\\\-->"
    replacement = f"<!--{tag}/-->{new_content}<!--{tag}\\\\-->"
    return re.sub(pattern, replacement, html_content, flags=re.DOTALL)

# Helper function for the skills section.
def map_level_to_class(level):
    if level == "Advanced":
        return "skills__80"
    elif level == "Intermediate":
        return "skills__60"
    elif level == "Beginner":
        return "skills__20"
    else:
        return ""

# Generating complex sections
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
def update_html_with_json_data(json_data, html_input_path, html_output_path):

    ############ Open the HTML : ############
    with open(html_input_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    ############ Replacing basic attributes : ############
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
    
    ############ Replacing complex sections : ############
    sections = ""
    sections += generate_skills_section(json_data["skills"])
    sections += generate_qualifications_section(json_data["education"], json_data["workExperience"])
    sections += generate_testimonials_section(json_data["testimonials"])
    html_content = replace_tagged_content(html_content, "AUTOGENERATED", sections)

    ############ Save the HTML : ############
    with open(html_output_path, 'w', encoding='utf-8') as file:
        print("completed task - HTML")
        file.write(html_content)

def export_latex_with_json_data(json_data, latex_output_path):
    StringCore1 = r"""\documentclass[11pt,a4paper,roman]{moderncv}        % possible options include font size ('10pt', '11pt' and '12pt'), paper size ('a4paper', 'letterpaper', 'a5paper', 'legalpaper', 'executivepaper' and 'landscape') and font family ('sans' and 'roman')
    \moderncvstyle{banking}                            % style options are 'casual' (default), 'classic', 'oldstyle' and 'banking'
    \moderncvcolor{blue}                                % color options 'blue' (default), 'orange', 'green', 'red', 'purple', 'grey' and 'black'
    \nopagenumbers{}                                  % uncomment to suppress automatic page numbering for CVs longer than one page
    \usepackage[utf8]{inputenc}
    \usepackage{fontawesome}
    \usepackage{fontspec}
    \usepackage{tabularx}
    \usepackage{ragged2e}
    \usepackage[scale=0.9]{geometry}
    \usepackage{multicol}
    \usepackage{import}
    \usepackage{color}
    \definecolor{DarkBlue}{rgb}{0, 0, 0.7}
    \newcommand*{\customcventry}[7][.25em]{
    \begin{tabular}{@{}l} 
        {\bfseries #4}
    \end{tabular}
    \hfill% move it to the right
    \begin{tabular}{l@{}}
        {\bfseries #5}
    \end{tabular} \\
    \begin{tabular}{@{}l} 
        {\itshape #3}
    \end{tabular}
    \hfill% move it to the right
    \begin{tabular}{l@{}}
        {\itshape #2}
    \end{tabular}
    \ifx&#7&%
    \else{\\%
        \begin{minipage}{\maincolumnwidth}%
        \footnotesize #7%
        \end{minipage}}\fi%
    \par\addvspace{#1}}
    \newcommand*{\customcvproject}[4][.25em]{
    %   \vfill\noindent
    \begin{tabular}{@{}l} 
        {\small\bfseries #2} % Apply small font size to the project title
    \end{tabular}
    \hfill% move it to the right
    \begin{tabular}{l@{}}
        {\footnotesize\itshape #3} % Apply small font size to the project date
    \end{tabular}
    \ifx&#4&%
    \else{\\%
        \begin{minipage}{\maincolumnwidth}%
        \footnotesize #4 %Apply small font size to the project description
        \end{minipage}}\fi%
    \par\addvspace{#1}}
    \setlength{\tabcolsep}{12pt}"""

    NameAddressTitle = f"""
    % Personal Data/ %
    \\name{{{json_data['personalInfo']['surname']}}}{{{json_data['personalInfo']['lastname']}}}
    \\address{{{json_data['personalInfo']['contact']['address']}}}
    % Personal Data\\ %

    \\begin{{document}}

    \\makecvtitle
    \\vspace*{{-23mm}}
    """

    # Extracting contect line infos from JSON
    languages = ', '.join(json_data['personalInfo']['languages'])
    email = json_data['personalInfo']['contact']['email']
    phone = json_data['personalInfo']['contact']['phone']
    github = json_data['socialLinks']['github']

    contact_line = f"""
    \\begin{{center}}
    \\begin{{tabular}}{{ c c c c }}
    % Contact line/ %
    \\faLanguage\\enspace {languages} &\\faEnvelopeO\\enspace {email} & \\faGithub\\enspace \\href{{{github}}}{{GitHub}} & \\faMobile\\enspace {phone} \\\\
    % Contact Line\\ %
    \\end{{tabular}}
    \\end{{center}}
    """

    about_section = f"""
    \\section{{ABOUT}}
    % About Section/ %
    {json_data['home']['description']}
    % About Section\\ %
    """
    # Formatting skills sections
    programming_skills = ', '.join(json_data["resumeSkills"]["programming"])
    data_skills = ', '.join(json_data["resumeSkills"]["data"])
    miscellaneous_skills = ', '.join(json_data["resumeSkills"]["miscellaneous"])

    skills_section = f"""
    \\section{{SKILLS}}
    % Resume Skills/ %
    \\textbf{{Programming:}} {programming_skills}\\\\*
    \\textbf{{Data:}} {data_skills}\\\\*
    \\textbf{{Miscellaneous:}} {miscellaneous_skills}
    % Resume Skills\\ %
    """
    # Formatting education section
    education_section = "\\section{EDUCATION}\n% Education/ %\n"
    for edu in json_data["education"]:
        degree_field = f"{edu['degree']} in {edu['field']}"  # Concatenate degree and field
        education_section += f"{{\\customcventry{{{edu['year']}}}{{{degree_field}}}{{{edu['institution']}}}{{}}{{}}\n{{"
        education_section += f"{edu['details']}}}\n}}\n"
    education_section += "% Education\\ %\n"


    experience_section = "\\section{EXPERIENCE}\n% Experience/ %\n"
    for exp in json_data["workExperience"]:
        experience_section += f"{{\\customcventry{{{exp['years']}}}{{{exp['position']}}}{{{exp['company']}}}{{Montreal, QC}}{{}}\n{{\\begin{{itemize}}\n"
        for detail in exp["resumeDetails"].split('. '):
            experience_section += f"    \\item {detail}\n"
        experience_section += "\\end{itemize}\n}}\n"
    experience_section += "% Experience\\ %\n"

    projects_section = "\\section{PROJECTS}\n% Projects/ %\n"
    for project in json_data["projects"]:
        project_details = project["description"].split('. ')
        projects_section += f"{{\\customcvproject{{{project['name']}}}{{}}\n{{\\begin{{itemize}}\n"
        for detail in project_details:
            projects_section += f"  \\item {detail}\n"
        projects_section += "\\end{itemize}\n}}\n"
    projects_section += "% Projects\\ %\n"

    latex_document = StringCore1+NameAddressTitle+contact_line+about_section+skills_section+education_section+experience_section+projects_section+"\end{document}"
    # Write the LaTeX document to a file
    with open(latex_output_path, 'w') as file:
        print("completed task - LATEX")
        file.write(latex_document)

#################################
# 1. Load the JSON : 
json_data = {}
with open('data.json', 'r') as file:
    json_data = json.load(file)

# 2. Load CSS, HTML Input and Output paths : 
css_input_path = 'assets/css/styles.css'
css_output_path = 'assets/css/styles.css'
html_input_path = 'input.html'
html_output_path = 'index.html'
latex_output_path = 'main.tex'

# 3. Update the CSS with json colors data :
update_css_with_json_colors(json_data, css_input_path, css_output_path)

# 4. Update the HTML with json data :
update_html_with_json_data(json_data, html_input_path, html_output_path)

# 5. Generate LaTeX file from json data : 
export_latex_with_json_data(json_data,  latex_output_path)


