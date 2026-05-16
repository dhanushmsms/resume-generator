MODERN_RESUME = r"""
\documentclass[a4paper,10pt]{article}
\usepackage[top=1.2cm, bottom=1.2cm, left=1.2cm, right=1.2cm]{geometry}
\usepackage{xcolor}
\usepackage{array}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{titlesec}
\usepackage{fontenc}
\usepackage{inputenc}
\usepackage{paracol}
\usepackage{graphicx}
\usepackage{mdframed}

\definecolor{sidebar}{HTML}{2D4A6B}
\definecolor{sidetext}{HTML}{FFFFFF}
\definecolor{accent}{HTML}{2D4A6B}
\definecolor{lightgray}{HTML}{F5F5F5}

\hypersetup{colorlinks=true, urlcolor=accent, linkcolor=accent}
\pagestyle{empty}
\setlength{\parindent}{0pt}

\newcommand{\sideheading}[1]{{\color{white}\large\bfseries\MakeUppercase{#1}}\vspace{4pt}\\\color{white!60!sidebar}\hrule\color{white}\vspace{6pt}}
\newcommand{\mainheading}[1]{\vspace{8pt}{\color{accent}\large\bfseries\MakeUppercase{#1}}\vspace{2pt}\\\color{accent}\hrule\color{black}\vspace{4pt}}
\newcommand{\jobtitle}[4]{{\bfseries #1} \hfill {\small #2}\\{\small\itshape #3} \hfill {\small\itshape #4}\vspace{2pt}}

\begin{document}

\columnratio{0.32}
\setlength{\columnsep}{0pt}

\begin{paracol}{2}

%% ---- LEFT SIDEBAR ----
\backgroundcolor{c[0](4pt,4pt)(0.5\columnsep,4pt)}{sidebar}
{\color{sidetext}
\vspace{12pt}
\begin{center}
{\huge\bfseries FULL NAME}\\[4pt]
{\small\color{white!80!sidebar} Job Title}
\end{center}
\vspace{10pt}

\sideheading{Contact}
{\small
Location\\[3pt]
Phone\\[3pt]
\href{mailto:email}{email}\\[3pt]
\href{linkedin}{LinkedIn}
}
\vspace{10pt}

\sideheading{Skills}
{\small
\begin{itemize}[leftmargin=8pt, itemsep=2pt, parsep=0pt]
  \item Skill One
  \item Skill Two
  \item Skill Three
  \item Skill Four
  \item Skill Five
\end{itemize}
}
\vspace{10pt}

\sideheading{Certifications}
{\small
\begin{itemize}[leftmargin=8pt, itemsep=2pt, parsep=0pt]
  \item Certification One
  \item Certification Two
\end{itemize}
}
\vspace{10pt}

\sideheading{Languages}
{\small
Language 1 -- Fluent\\[3pt]
Language 2 -- Fluent
}
}

\switchcolumn

%% ---- RIGHT MAIN CONTENT ----
\vspace{8pt}
\hspace{8pt}
\begin{minipage}[t]{0.95\linewidth}

\mainheading{Professional Summary}
{\small Summary text goes here.}

\mainheading{Work Experience}
\jobtitle{Job Title}{MM/YYYY -- Present}{Company Name}{Location}
\begin{itemize}[leftmargin=12pt, itemsep=1pt, parsep=0pt]
  \small
  \item Bullet point one describing achievement with metrics.
  \item Bullet point two describing another achievement.
  \item Bullet point three.
\end{itemize}

\vspace{4pt}
\jobtitle{Job Title 2}{MM/YYYY -- MM/YYYY}{Company Name 2}{Location}
\begin{itemize}[leftmargin=12pt, itemsep=1pt, parsep=0pt]
  \small
  \item Bullet point one.
  \item Bullet point two.
\end{itemize}

\mainheading{Education}
\jobtitle{Degree Name}{MM/YYYY -- MM/YYYY}{University Name}{Location, Country}
{\small Grade: Distinction}

\vspace{4pt}
\jobtitle{Degree Name 2}{MM/YYYY -- MM/YYYY}{University Name 2}{Location, Country}
{\small Grade: First Class}

\mainheading{Achievements}
\begin{itemize}[leftmargin=12pt, itemsep=1pt, parsep=0pt]
  \small
  \item Achievement one.
  \item Achievement two.
\end{itemize}

\end{minipage}

\end{paracol}

\end{document}
"""

CLASSIC_RESUME = r"""
\documentclass[a4paper,11pt]{article}
\usepackage[top=2cm, bottom=2cm, left=2.2cm, right=2.2cm]{geometry}
\usepackage{xcolor}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{titlesec}
\usepackage{fontenc}
\usepackage{inputenc}

\definecolor{darkgray}{HTML}{333333}
\definecolor{midgray}{HTML}{555555}

\hypersetup{colorlinks=true, urlcolor=darkgray, linkcolor=darkgray}
\pagestyle{empty}
\setlength{\parindent}{0pt}

\titleformat{\section}{\large\bfseries\color{darkgray}}{}{0em}{}[\titlerule]
\titlespacing{\section}{0pt}{10pt}{6pt}

\newcommand{\jobtitle}[4]{{\bfseries #1}\hfill{\small #2}\\{\small\color{midgray}\itshape #3}\hfill{\small\color{midgray}\itshape #4}}

\begin{document}

\begin{center}
  {\Huge\bfseries\color{darkgray} FULL NAME}\\[6pt]
  {\small Location \textbullet{} Phone \textbullet{} \href{mailto:email}{email} \textbullet{} \href{linkedin}{LinkedIn}}
\end{center}

\vspace{4pt}

\section*{Professional Summary}
{\small Summary text goes here describing the candidate's background, key skills, and what they bring to the role.}

\section*{Work Experience}
\jobtitle{Job Title}{MM/YYYY -- Present}{Company Name}{Location}
\begin{itemize}[leftmargin=16pt, itemsep=2pt, parsep=0pt, topsep=4pt]
  \small
  \item Bullet point one describing a key achievement with measurable impact.
  \item Bullet point two describing another responsibility or accomplishment.
  \item Bullet point three.
\end{itemize}

\vspace{6pt}
\jobtitle{Job Title 2}{MM/YYYY -- MM/YYYY}{Company Name 2}{Location}
\begin{itemize}[leftmargin=16pt, itemsep=2pt, parsep=0pt, topsep=4pt]
  \small
  \item Bullet point one.
  \item Bullet point two.
\end{itemize}

\section*{Education}
\jobtitle{Degree Name}{MM/YYYY -- MM/YYYY}{University Name}{Location}\\[2pt]
{\small Grade: Distinction. Key modules: Module 1, Module 2, Module 3.}

\vspace{6pt}
\jobtitle{Degree Name 2}{MM/YYYY -- MM/YYYY}{University Name 2}{Location}\\[2pt]
{\small Grade: First Class.}

\section*{Technical Skills}
{\small \textbf{Analytics \& Tools:} Skill 1, Skill 2, Skill 3, Skill 4\\
\textbf{Programming:} Language 1, Language 2\\
\textbf{Soft Skills:} Communication, Teamwork, Leadership}

\section*{Certifications}
\begin{itemize}[leftmargin=16pt, itemsep=2pt, parsep=0pt, topsep=2pt]
  \small
  \item Certification One -- Provider (Year)
  \item Certification Two -- Provider (Year)
\end{itemize}

\section*{Achievements}
\begin{itemize}[leftmargin=16pt, itemsep=2pt, parsep=0pt, topsep=2pt]
  \small
  \item Achievement one with context.
  \item Achievement two with context.
\end{itemize}

\section*{Languages}
{\small Language 1 -- Fluent \quad Language 2 -- Fluent}

\end{document}
"""

MINIMAL_RESUME = r"""
\documentclass[a4paper,10.5pt]{article}
\usepackage[top=1.8cm, bottom=1.8cm, left=2cm, right=2cm]{geometry}
\usepackage{xcolor}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{fontenc}
\usepackage{inputenc}

\definecolor{accentgray}{HTML}{666666}
\definecolor{linecolor}{HTML}{CCCCCC}

\hypersetup{colorlinks=true, urlcolor=accentgray}
\pagestyle{empty}
\setlength{\parindent}{0pt}

\newcommand{\msection}[1]{\vspace{10pt}{\color{accentgray}\small\MakeUppercase{\bfseries #1}}\vspace{2pt}\\\textcolor{linecolor}{\hrule}\vspace{4pt}}
\newcommand{\jobtitle}[4]{{\bfseries #1} \hfill {\small\color{accentgray} #2}\\{\small\color{accentgray}\itshape #3, #4}}

\begin{document}

{\huge FULL NAME}\\[4pt]
{\small\color{accentgray} Location \quad|\quad Phone \quad|\quad \href{mailto:email}{email} \quad|\quad \href{linkedin}{LinkedIn}}

\msection{Summary}
{\small Summary text goes here.}

\msection{Experience}
\jobtitle{Job Title}{MM/YYYY -- Present}{Company Name}{Location}
\begin{itemize}[leftmargin=12pt, itemsep=1pt, parsep=0pt, topsep=3pt]
  \small
  \item[\textendash] Bullet point one with measurable impact.
  \item[\textendash] Bullet point two.
  \item[\textendash] Bullet point three.
\end{itemize}

\vspace{4pt}
\jobtitle{Job Title 2}{MM/YYYY -- MM/YYYY}{Company Name 2}{Location}
\begin{itemize}[leftmargin=12pt, itemsep=1pt, parsep=0pt, topsep=3pt]
  \small
  \item[\textendash] Bullet point one.
  \item[\textendash] Bullet point two.
\end{itemize}

\msection{Education}
\jobtitle{Degree Name}{MM/YYYY -- MM/YYYY}{University Name}{Location}\\[2pt]
{\small\color{accentgray} Distinction}

\vspace{4pt}
\jobtitle{Degree Name 2}{MM/YYYY -- MM/YYYY}{University Name 2}{Location}\\[2pt]
{\small\color{accentgray} First Class}

\msection{Skills}
{\small Skill 1 \textbullet{} Skill 2 \textbullet{} Skill 3 \textbullet{} Skill 4 \textbullet{} Skill 5 \textbullet{} Skill 6 \textbullet{} Skill 7}

\msection{Achievements}
\begin{itemize}[leftmargin=12pt, itemsep=1pt, parsep=0pt, topsep=2pt]
  \small
  \item[\textendash] Achievement one.
  \item[\textendash] Achievement two.
\end{itemize}

\msection{Languages}
{\small Language 1 -- Fluent \quad Language 2 -- Fluent}

\end{document}
"""

MODERN_COVER = r"""
\documentclass[a4paper,10pt]{article}
\usepackage[top=1.2cm, bottom=1.2cm, left=1.2cm, right=1.2cm]{geometry}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{fontenc}
\usepackage{inputenc}
\usepackage{paracol}

\definecolor{sidebar}{HTML}{2D4A6B}
\definecolor{sidetext}{HTML}{FFFFFF}
\definecolor{accent}{HTML}{2D4A6B}

\hypersetup{colorlinks=true, urlcolor=accent}
\pagestyle{empty}
\setlength{\parindent}{0pt}

\newcommand{\sideheading}[1]{{\color{white}\large\bfseries\MakeUppercase{#1}}\vspace{4pt}\\\color{white!60!sidebar}\hrule\color{white}\vspace{6pt}}

\begin{document}

\columnratio{0.32}
\setlength{\columnsep}{0pt}

\begin{paracol}{2}

%% ---- LEFT SIDEBAR ----
\backgroundcolor{c[0](4pt,4pt)(0.5\columnsep,4pt)}{sidebar}
{\color{sidetext}
\vspace{12pt}
\begin{center}
  {\huge\bfseries FULL NAME}\\[4pt]
  {\small\color{white!80!sidebar} Job Title}
\end{center}
\vspace{10pt}

\sideheading{Contact}
{\small
Location\\[3pt]
Phone\\[3pt]
\href{mailto:email}{email}\\[3pt]
\href{linkedin}{LinkedIn}
}
\vspace{10pt}

\sideheading{Key Skills}
{\small
\begin{itemize}[leftmargin=8pt, itemsep=2pt, parsep=0pt]
  \item Skill One
  \item Skill Two
  \item Skill Three
  \item Skill Four
\end{itemize}
}
}

\switchcolumn

%% ---- RIGHT LETTER CONTENT ----
\vspace{8pt}
\hspace{8pt}
\begin{minipage}[t]{0.95\linewidth}

\vspace{6pt}
{\small Today's Date}

\vspace{10pt}
{\bfseries Hiring Manager}\\
{\small Company Name}\\
{\small Company Address}

\vspace{12pt}
{\bfseries\color{accent}\large Re: Application for Job Title}

\vspace{10pt}
{\small Dear Hiring Manager,}

\vspace{8pt}
{\small Opening paragraph: express enthusiasm for the role and company. Mention how you found the position and give a brief summary of why you are a strong candidate.}

\vspace{8pt}
{\small Second paragraph: highlight 2-3 specific achievements or experiences directly relevant to the job description. Use metrics and concrete examples.}

\vspace{8pt}
{\small Third paragraph: connect your skills and values to the company's mission or culture. Show you have researched the company.}

\vspace{8pt}
{\small Closing paragraph: thank the reader, express eagerness for an interview, and include a call to action.}

\vspace{12pt}
{\small Yours sincerely,}

\vspace{10pt}
{\bfseries FULL NAME}

\end{minipage}

\end{paracol}

\end{document}
"""

CLASSIC_COVER = r"""
\documentclass[a4paper,11pt]{article}
\usepackage[top=2.5cm, bottom=2.5cm, left=2.5cm, right=2.5cm]{geometry}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{fontenc}
\usepackage{inputenc}

\definecolor{darkgray}{HTML}{333333}

\hypersetup{colorlinks=true, urlcolor=darkgray}
\pagestyle{empty}
\setlength{\parindent}{0pt}

\begin{document}

{\bfseries\large\color{darkgray} FULL NAME}\\[2pt]
{\small Location \quad Phone \quad \href{mailto:email}{email} \quad \href{linkedin}{LinkedIn}}\\[2pt]
\textcolor{darkgray}{\hrule}

\vspace{16pt}
{\small Today's Date}

\vspace{16pt}
{\small Hiring Manager\\
Company Name\\
Company Address}

\vspace{16pt}
{\bfseries Re: Application for Job Title}

\vspace{12pt}
{\small Dear Hiring Manager,}

\vspace{10pt}
{\small Opening paragraph: express enthusiasm for the role and company. Briefly summarise why you are an excellent fit, referencing where you found the position.}

\vspace{10pt}
{\small Second paragraph: present 2-3 specific, measurable achievements that are directly relevant to the role. Demonstrate the value you bring.}

\vspace{10pt}
{\small Third paragraph: connect your background and values to the company's goals or culture. Show you have done your research.}

\vspace{10pt}
{\small Closing paragraph: thank the reader for their time, express enthusiasm for the opportunity to discuss your application, and provide a clear call to action.}

\vspace{16pt}
{\small Yours sincerely,}

\vspace{24pt}
{\bfseries FULL NAME}

\end{document}
"""

MINIMAL_COVER = r"""
\documentclass[a4paper,10.5pt]{article}
\usepackage[top=2cm, bottom=2cm, left=2.5cm, right=2.5cm]{geometry}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{fontenc}
\usepackage{inputenc}

\definecolor{accentgray}{HTML}{666666}
\definecolor{linecolor}{HTML}{CCCCCC}

\hypersetup{colorlinks=true, urlcolor=accentgray}
\pagestyle{empty}
\setlength{\parindent}{0pt}

\begin{document}

{\huge FULL NAME}\\[4pt]
{\small\color{accentgray} Location \quad|\quad Phone \quad|\quad \href{mailto:email}{email} \quad|\quad \href{linkedin}{LinkedIn}}
\vspace{4pt}
\textcolor{linecolor}{\hrule}

\vspace{14pt}
{\small\color{accentgray} Today's Date}

\vspace{14pt}
{\small Hiring Manager\\
Company Name}

\vspace{14pt}
{\bfseries Application for Job Title}

\vspace{10pt}
{\small Dear Hiring Manager,}

\vspace{8pt}
{\small Opening paragraph: introduce yourself and express genuine enthusiasm for the role. State why this company and position appeal to you.}

\vspace{8pt}
{\small Second paragraph: highlight 2-3 specific achievements with metrics that match the key requirements in the job description.}

\vspace{8pt}
{\small Third paragraph: show alignment with the company's values or mission. Keep it concise and authentic.}

\vspace{8pt}
{\small Closing paragraph: thank the reader and invite further conversation. Keep it direct and confident.}

\vspace{14pt}
{\small Sincerely,}

\vspace{18pt}
{\bfseries FULL NAME}\\
{\small\color{accentgray} Phone | \href{mailto:email}{email}}

\end{document}
"""

TEMPLATES = {
    "Modern": {
        "resume": MODERN_RESUME,
        "cover_letter": MODERN_COVER,
        "description": "Two-column with dark navy sidebar",
        "features": ["Coloured sidebar", "Bold section headings", "Icon-style layout"],
        "color": "#2D4A6B",
        "preview_html": """
        <div style="width:100%;height:140px;border-radius:8px;overflow:hidden;border:1px solid #ddd;display:flex;">
          <div style="width:32%;background:#2D4A6B;padding:8px;">
            <div style="background:rgba(255,255,255,0.9);height:18px;border-radius:3px;margin-bottom:6px;width:80%;margin-left:auto;margin-right:auto;"></div>
            <div style="background:rgba(255,255,255,0.5);height:6px;border-radius:2px;margin-bottom:4px;width:90%;"></div>
            <div style="background:rgba(255,255,255,0.3);height:4px;border-radius:2px;margin-bottom:3px;width:85%;"></div>
            <div style="background:rgba(255,255,255,0.3);height:4px;border-radius:2px;margin-bottom:3px;width:75%;"></div>
            <div style="background:rgba(255,255,255,0.3);height:4px;border-radius:2px;width:80%;"></div>
            <div style="margin-top:8px;background:rgba(255,255,255,0.5);height:6px;border-radius:2px;margin-bottom:4px;width:60%;"></div>
            <div style="background:rgba(255,255,255,0.3);height:4px;border-radius:2px;margin-bottom:3px;width:85%;"></div>
            <div style="background:rgba(255,255,255,0.3);height:4px;border-radius:2px;width:70%;"></div>
          </div>
          <div style="width:68%;padding:8px;background:white;">
            <div style="background:#2D4A6B;height:5px;border-radius:2px;margin-bottom:6px;width:50%;"></div>
            <div style="background:#eee;height:4px;border-radius:2px;margin-bottom:3px;width:95%;"></div>
            <div style="background:#eee;height:4px;border-radius:2px;margin-bottom:8px;width:80%;"></div>
            <div style="background:#2D4A6B;height:5px;border-radius:2px;margin-bottom:6px;width:60%;"></div>
            <div style="background:#ddd;height:4px;border-radius:2px;margin-bottom:2px;width:90%;"></div>
            <div style="background:#eee;height:4px;border-radius:2px;margin-bottom:2px;width:95%;"></div>
            <div style="background:#eee;height:4px;border-radius:2px;margin-bottom:2px;width:85%;"></div>
            <div style="background:#eee;height:4px;border-radius:2px;width:75%;"></div>
          </div>
        </div>
        """
    },
    "Classic": {
        "resume": CLASSIC_RESUME,
        "cover_letter": CLASSIC_COVER,
        "description": "Traditional single-column, formal",
        "features": ["Centered header", "Horizontal dividers", "Professional serif style"],
        "color": "#333333",
        "preview_html": """
        <div style="width:100%;height:140px;border-radius:8px;overflow:hidden;border:1px solid #ddd;background:white;padding:10px;box-sizing:border-box;">
          <div style="background:#333;height:14px;border-radius:2px;margin:0 auto 4px;width:45%;"></div>
          <div style="background:#999;height:5px;border-radius:2px;margin:0 auto 6px;width:60%;"></div>
          <div style="background:#333;height:1px;width:100%;margin-bottom:6px;"></div>
          <div style="background:#555;height:6px;border-radius:2px;margin-bottom:4px;width:35%;"></div>
          <div style="background:#eee;height:4px;border-radius:2px;margin-bottom:3px;width:100%;"></div>
          <div style="background:#eee;height:4px;border-radius:2px;margin-bottom:6px;width:85%;"></div>
          <div style="background:#333;height:1px;width:100%;margin-bottom:6px;"></div>
          <div style="background:#555;height:6px;border-radius:2px;margin-bottom:4px;width:40%;"></div>
          <div style="background:#eee;height:4px;border-radius:2px;margin-bottom:3px;width:100%;"></div>
          <div style="background:#eee;height:4px;border-radius:2px;margin-bottom:3px;width:90%;"></div>
          <div style="background:#eee;height:4px;border-radius:2px;width:80%;"></div>
        </div>
        """
    },
    "Minimal": {
        "resume": MINIMAL_RESUME,
        "cover_letter": MINIMAL_COVER,
        "description": "Clean, spacious, modern minimalist",
        "features": ["Lots of whitespace", "Subtle gray accents", "Easy to read"],
        "color": "#666666",
        "preview_html": """
        <div style="width:100%;height:140px;border-radius:8px;overflow:hidden;border:1px solid #ddd;background:white;padding:10px;box-sizing:border-box;">
          <div style="background:#333;height:12px;border-radius:2px;margin-bottom:3px;width:40%;"></div>
          <div style="background:#bbb;height:4px;border-radius:2px;margin-bottom:6px;width:65%;"></div>
          <div style="background:#ccc;height:1px;width:100%;margin-bottom:7px;"></div>
          <div style="background:#999;height:5px;border-radius:2px;margin-bottom:4px;width:20%;"></div>
          <div style="background:#eee;height:3px;border-radius:2px;margin-bottom:2px;width:100%;"></div>
          <div style="background:#eee;height:3px;border-radius:2px;margin-bottom:6px;width:80%;"></div>
          <div style="background:#ccc;height:1px;width:100%;margin-bottom:7px;"></div>
          <div style="background:#999;height:5px;border-radius:2px;margin-bottom:4px;width:25%;"></div>
          <div style="background:#eee;height:3px;border-radius:2px;margin-bottom:2px;width:100%;"></div>
          <div style="background:#eee;height:3px;border-radius:2px;margin-bottom:2px;width:90%;"></div>
          <div style="background:#eee;height:3px;border-radius:2px;width:75%;"></div>
        </div>
        """
    }
}
