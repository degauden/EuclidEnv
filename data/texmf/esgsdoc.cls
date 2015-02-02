%%------------------------------------------------------------
%% General Euclid SGS document class
%%------------------------------------------------------------
%%
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{esgsdoc}[2014/02/07 v0.1 Euclid document class]

\LoadClass[12pt,a4paper]{article}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{amsbsy}
\RequirePackage{times}
\RequirePackage{ifthen}
\RequirePackage{calc}
\RequirePackage{array}
\RequirePackage{fancyhdr}
\RequirePackage{multirow}
\RequirePackage{float}
\RequirePackage{graphicx}
\RequirePackage{longtable}
\RequirePackage{eso-pic}
\RequirePackage{color}
\RequirePackage{type1cm}
\RequirePackage{hyperref}
\RequirePackage{breakurl}
\RequirePackage{natbib}
\RequirePackage{numprint}
\RequirePackage{tabularx}
\RequirePackage{ragged2e}
\RequirePackage{xcolor} 
\RequirePackage{colortbl} 
\RequirePackage{hyphenat} 
\RequirePackage{lastpage} 
\RequirePackage[UKenglish,num]{isodate}
%\RequirePackage{mathptmx} % note this messes up \vec definition... do not e add put in your doc if you want it


% Switch off the onecolumn and twocolumn options
\DeclareOption{onecolumn}{\OptionNotUsed}
\DeclareOption{twocolumn}{\OptionNotUsed}

%
%    DRAFT
%------------------------------------------------------------
%%
\DeclareOption{esgsdraft}{
    % DRAFT
    \AddToShipoutPicture{%
            \setlength{\unitlength}{0.6pt}%
        \makeatletter
            \put(\strip@pt \textwidth,\strip@pt \textheight){%
                \makebox(0,0){%
                \rotatebox{45}{%
                    \textcolor[gray]{0.95}{%
                        \fontsize{5cm}{5cm}\textsf{Draft}%
                    }}}}%
        \makeatother
    }%
}

%
% Define the various ESGS document types
%------------------------------------------------------------
%
% \DeclareOption{CP}{
%    \renewcommand{\esgsDocType}{Conference Proceeding}
% }
% \DeclareOption{MN}{
%    \renewcommand{\esgsDocType}{Meeting Minutes}
% }
% \DeclareOption{PR}{
%    \renewcommand{\esgsDocType}{Progress Report}
% }
% \DeclareOption{SP}{
%    \renewcommand{\esgsDocType}{Specification}
% }
\DeclareOption{TN}{
   \renewcommand{\esgsDocType}{Technical Note}
}
% \DeclareOption{TR}{
%    \renewcommand{\esgsDocType}{Test Report}
% }
% \DeclareOption{SDP}{
%    \renewcommand{\esgsDocType}{Software Development Plan}
% }
% \DeclareOption{DDP}{
%    \renewcommand{\esgsDocType}{Data Processing Centre Development Plan}
% }
% \DeclareOption{SRS}{
%    \renewcommand{\esgsDocType}{Software Requirement Specifications}
% }
\DeclareOption{SDD}{
   \renewcommand{\esgsDocType}{Software Design Document}
}
% \DeclareOption{ICD}{
%    \renewcommand{\esgsDocType}{Interface Control Document}
% }
% \DeclareOption{SUM}{
%    \renewcommand{\esgsDocType}{Software User Manual}
% }
% \DeclareOption{SRN}{
%    \renewcommand{\esgsDocType}{Software Release Note}
% }
% \DeclareOption{STP}{
%    \renewcommand{\esgsDocType}{System Validation and Test Plan}
% }
% \DeclareOption{STS}{
%    \renewcommand{\esgsDocType}{Software Test Specification}
% }
% \DeclareOption{STR}{
%    \renewcommand{\esgsDocType}{Software Test Report}
% }
% \DeclareOption{VTR}{
%    \renewcommand{\esgsDocType}{Validation Test Report}
% }
% \DeclareOption{SPAR}{
%    \renewcommand{\esgsDocType}{Software Product Assurance Report}
% } 
% \DeclareOption{PL}{
%    \renewcommand{\esgsDocType}{Planning and Policy Document}
% }
% \DeclareOption{UG}{
%    \renewcommand{\esgsDocType}{User Guide}
% }
% %there is only one of these probably
% \DeclareOption{SSS}{
%    \renewcommand{\esgsDocType}{Software System Specification}
% } 
 
%
% Define the \TEAM (SDCs or OUs) 
%------------------------------------------------------------
%
\newcommand{\TEAM}{SDCx}

\DeclareOption{SDCCH}{
   \renewcommand{\TEAM}{SDC-CH}
}
\DeclareOption{OUPHZ}{
   \renewcommand{\TEAM}{OU-PHZ}
}


%
% LOGO
%------------------------------------------------------------
%
\newcommand{\setEsaDocLogo}[1]{\def\@esaDocLogo{#1}}
\setEsaDocLogo{41_digital_logo_grey}

% This is when we will have a Euclid logo again!
\newcommand{\setEsgsDocLogo}[1]{\def\@esgsDocLogo{#1}}
\setEsgsDocLogo{EC_logo.png}

% you own DPC, institute or funding logo for front page
\newcommand{\setEsgsDocLocalLogo}[1]{\def\@esgsDocLocalLogo{#1}}
\setEsgsDocLocalLogo{}

%
% New commands for Header and Title page 
%------------------------------------------------------------
%
\newcommand{\esgsDocType}{Euclid SGS Document}

\newcommand{\esgsDocShortTitle}{set the Short Title with {$\backslash$}setEsgsDocShortTitle}
\newcommand{\setEsgsDocShortTitle}[1]{\renewcommand{\esgsDocShortTitle}{#1}}

\newcommand{\esgsDocTitle}{set the Title with {$\backslash$}setEsgsDocTitle}
\newcommand{\setEsgsDocTitle}[1]{\renewcommand{\esgsDocTitle}{#1}}

\newcommand{\esgsDocSubtitle}{No Subtitle}
\newcommand{\setEsgsDocSubtitle}[1]{\def\@esgsDocSubtitle{#1}
  \renewcommand{\esgsDocSubtitle}{#1}
}
\setEsgsDocSubtitle{}

%\setEsgsDocTitle{Set the document title with $\backslash$setEsgsDocTitle}
\newcommand{\esgsDocDate}{set the date with {$\backslash$}setEsgsDocDate}
\newcommand{\setEsgsDocDate}[1]{\renewcommand{\esgsDocDate}{#1}}

\newcommand{\esgsDocIssue}{none}
\newcommand{\setEsgsDocIssue}[1]{\renewcommand{\esgsDocIssue}{#1}}

\newcommand{\esgsDocStatus}{set the Status with {$\backslash$}setEsgsDocStatus}
\newcommand{\setEsgsDocStatus}[1]{\renewcommand{\esgsDocStatus}{#1}}

\newcommand{\esgsDocRevision}{set the Revision with {$\backslash$}setEsgsDocRevision}
\newcommand{\setEsgsDocRevision}[1]{\renewcommand{\esgsDocRevision}{#1}}

\newcommand{\esgsDocRef}{set the Reference with {$\backslash$}setEsgsDocRef}
\newcommand{\setEsgsDocRef}[1]{\renewcommand{\esgsDocRef}{#1}}

\newcommand{\esgsDocAuthor}{set the Author with {$\backslash$}setEsgsDocAuthor}
\newcommand{\setEsgsDocAuthor}[1]{\renewcommand{\esgsDocAuthor}{#1}}

\newcommand{\setEsgsDocCurator}[1]{\def\@esgsDocCurator{#1}}
\setEsgsDocCurator{}

\newcommand{\setEsgsDocAffil}[1]{\def\@esgsDocAffil{#1}}
\setEsgsDocAffil{}

\newcommand{\esgsDocApprove}{@noapprove@}
\newcommand{\setEsgsDocApprove}[1]{\renewcommand{\esgsDocApprove}{#1}}

\newcommand{\esgsDocAuthorize}{@noauthorize@}
\newcommand{\setEsgsDocAuthorize}[1]{\renewcommand{\esgsDocAuthorize}{#1}}

%
%   ABSTRACT
%------------------------------------------------------------
%
\newcommand{\esgsDocAbstract}{}
\newcommand{\setEsgsDocAbstract}[1]{\renewcommand{\esgsDocAbstract}
{\section*{Abstract}
    \ifx \@esgsDocCompact \@empty
           \vspace*{1cm}
     \else
           \relax
    \fi
    \begin{center}
    \parbox{.9\textwidth}{#1}\\
    \end{center}
    \pagebreak
}}

%
% Command \putlogo (not currently used)
%------------------------------------------------------------
%
\providecommand{\putlogo}{
    \ifx \@esgsDocLocalLogo \@empty
           \def\@lbsize{0.5}
     \else
           \def\@lbsize{0.75}
    \fi
  \begin{center}
   \resizebox{\@lbsize\textwidth}{!}{\includegraphics{\@esgsDocLogo}
   
    \ifx \@esgsDocLocalLogo \@empty
           \relax
     \else
           \includegraphics{\@esgsDocLocalLogo}
    \fi
   }
   \end{center}
}

\ProcessOptions\relax
%------------------------------------------------------------
% End of options processing
%------------------------------------------------------------

%
%  Definitions used in title page and headers
%------------------------------------------------------------
%
\newcolumntype{L}[1]{>{\raggedright\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\newcolumntype{C}[1]{>{\centering\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\newcolumntype{R}[1]{>{\raggedleft\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\definecolor{light-gray}{gray}{0.80}

\newcommand\T{\rule{0pt}{0.6cm}}       % Top strut
\newcommand\B{\rule[-0.4cm]{0pt}{0pt}} % Bottom strut

%------------------------------------------------------------
%  FIRST PAGE
%------------------------------------------------------------
%
% Title block definition
%------------------------------------------------------------
%
\providecommand{\mktitle}{

  \hypersetup{pdftitle={\esgsDocTitle\ifx\@esgsDocSubtitle\@empty\else\ - \esgsDocSubtitle\fi},
  pdfauthor={\esgsDocAuthor},
  pdfkeywords={\esgsDocRef}}
    
 \setlength{\parindent}{0pt}
  
\renewcommand{\arraystretch}{1.4}
\begin{tabular}{ | R{3.0cm} | p{3.8cm} | R{3.8cm} | p{3.8cm} |}
\hline
  {\bf Title: }           & \multicolumn{3}{|l|}{\parbox{11.2cm}{\esgsDocTitle} \T \B } \\ \hline
  {\bf Dates:}          & \esgsDocDate & {\bf Issue:} & \esgsDocIssue .\esgsDocRevision \\ \hline
  {\bf Reference: }  & \multicolumn{3}{|l|}{\esgsDocRef} \\ \hline
  {\bf Custodian:}   & \multicolumn{3}{|l|}{\esgsDocAuthor} \\ \hline
  \end{tabular}
\renewcommand{\arraystretch}{1.0}
\vspace*{1.2cm}
}

%
%   Doc People: Document contributors, authorization, agreement and approval
%---------------------------------------------------------------
%
\newenvironment{docPeople}[0]{
\renewcommand{\arraystretch}{1.2}
    \setlength\LTleft{0pt}
    \setlength\LTright{\fill}
%   \setlength\LTpost{\fill}
%   \addtocounter{table}{-1}
    \begin{longtable}{ | p{4.0cm} | p{4.9cm} | C{2.0cm} | C{3.5cm} |}

    \hline
    \endfirsthead
    \hline
    \endhead
    \multicolumn{4}{r}{\emph{Continued on next page}}
    \endfoot
    \endlastfoot
}{
\hline
\end{longtable}
\renewcommand{\arraystretch}{1.0}
}

\providecommand{\addPeopleGroup}[1]{
\hline\cellcolor{light-gray}  {\bf #1} &  \cellcolor{light-gray} & \cellcolor{light-gray} {\bf Date:}   &  \cellcolor{light-gray} {\bf  Signature:}  \\ \hline }

\providecommand{\addPeople}[4]{
  #1 & #2 & #3 & #4 \\}


%------------------------------------------------------------
%  SECOND PAGE
%------------------------------------------------------------
%
%   Document history
%------------------------------------------------------------
%
\newenvironment{docHistory}[0]{
  \newpage
  \section*{Document History}
  \begin{small}
    % flush table to the left
    \setlength\LTleft{0pt}
    \setlength\LTright{\fill}
%   \setlength\LTpost{\fill}
%   \addtocounter{table}{-1}
    \begin{longtable}{|C{0.8cm}|C{2cm}|C{1.2cm}|p{7.4cm}|p{4cm}|}
    \hline
 \rowcolor{light-gray}     Issue & Date & Page & Description Of Change & Comment \\ \hline
    \endfirsthead
    \hline
 \rowcolor{light-gray}     Issue & Date & Page & Description Of Change & Comment \\ \hline
    \endhead
    \multicolumn{5}{r}{\emph{Continued on next page}}
    \endfoot
    \endlastfoot
}{
\end{longtable}
\end{small}
%        \ifx \@esgsDocCompact \@empty
%           \pagebreak
%         \else
%         \relax
%        \fi
}

\providecommand{\addtohist}[5]{
#1 & #2 & #3 & #4 & #5\\\hline}


% 
% Issue Lists
%------------------------------------------------------------
%
\newenvironment{issueList}[0]{
\begin{longtable}{|l|p{0.8\textwidth}|}\hline \textbf{ID}&\textbf{Summary}\\\hline 
}{
\end{longtable}
}

\providecommand{\addissue}[2]{
#1 & #2\\\hline}


%------------------------------------------------------------
%  PAGE LAYOUT (with headers and footers)
%------------------------------------------------------------
\setlength{\textwidth}{18cm}
\setlength{\textheight}{21.5cm}

\setlength{\topmargin}{-1.5cm}
\setlength{\oddsidemargin}{-1.0cm}
\setlength{\evensidemargin}{-1.0cm}
\setlength{\leftmargin}{0cm}
\setlength{\marginparwidth}{2cm}

\setlength{\parindent}{0cm}             % No indent at start of paragraphs
\setlength{\parskip}{\baselineskip}     % Blank line between paragraph

\setlength\headheight{2.85cm}     % Make space for logo

\pagenumbering{arabic}
\mark{{}{}} 

\newcommand{\clearemptydoublepage}{\newpage{\pagestyle{empty}\cleardoublepage}}

%% min page fraction that must be filled with text
\renewcommand{\textfraction}{0.1} 
%% max page fraction that a float may take at the top of the page
\renewcommand{\topfraction}{0.9} 
%% max page fraction that a float may take at the bottom of the page
\renewcommand{\bottomfraction}{0.9}
%% max page fraction that may be filled with floats
\renewcommand{\floatpagefraction}{0.5}
%% maximum number of floats at the top of the page
\setcounter{topnumber}{3}
%% maximum number of floats at the bottom of the page
\setcounter{bottomnumber}{1}
%% maximum total number of floats on a page
\setcounter{totalnumber}{5}

\def\fps@figure{!htbp}

\setcounter{secnumdepth}{5}    % numbering level of sections
\setcounter{tocdepth}{4}       % appearance level in table of contents

%
%  Customizing the page layout, header and footer  with fancyhdr
%------------------------------------------------------------
%
% http://en.wikibooks.org/wiki/LaTeX/Page_Layout#Customizing_with_fancyhdr
%
\pagestyle{fancy}
%
% make space for the header boxes
%
\addtolength{\headsep}{0cm} 
%
% Remove the default horizontal lines separating header and footer
% from the text body
%
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
%
%   Header definition
%------------------------------------------------------------
%

\lhead{}
\chead{
\begin{footnotesize}
\renewcommand{\arraystretch}{1.0}
%\newcommand\T{\rule{0pt}{0.6cm}}       % Top strut
%\newcommand\B{\rule[-0.4cm]{0pt}{0pt}} % Bottom strut
\hspace*{-0.4cm}\begin{tabular}{ | C{3.0cm} | C{8.6cm} | p{1.3cm} p{4.4cm} |}
\hline
\multirow{2}{*}[0.4cm]{\resizebox{2.6cm}{!}{\includegraphics{\@esaDocLogo}}} & \multirow{4}{*}{\parbox[c]{8.2cm}{\textit{\Large\bf \esgsDocShortTitle }}}
& Ref: & \esgsDocRef \T \\
                                 &         & Issue: & \esgsDocIssue .\esgsDocRevision \\
\cline{1-1}
\multirow{2}{*}[-0.04cm]{\resizebox{1.98cm}{!}{\includegraphics{\@esgsDocLogo}}} &  & Date: & \esgsDocDate \\
& & Page: & \thepage/\pageref{LastPage} \B \\
\hline
\end{tabular}
\renewcommand{\arraystretch}{1.0}
\end{footnotesize}
}
\rhead{}

%
%   Footer definition
%------------------------------------------------------------
%
%\renewcommand{\footrulewidth}{0.4pt}
\lfoot{}
\cfoot{
\begin{center}
\begin{scriptsize}
The presented document is Proprietary information of the Euclid
Science Ground Segment, a collaboration between ESA and the Euclid
Consortium. \\
This document shall be used and disclosed by the receiving Party and
its related entities (e.g. contractors and subcontractors) only for
the purposes of \\
fulfilling the receiving Party's responsibilities under the Euclid
Project and that the identified and marked technical data shall not be
disclosed or \\[-0.22cm]
retransferred to any other entity without prior written permission of the document preparer.
\end{scriptsize}
\end{center}
}
\rfoot{}

%------------------------------------------------------------
%  SECTIONING
%------------------------------------------------------------
\renewcommand{\section}{\@startsection
  {section}%                                    % the name
  {1}%                                          % the level
  {0mm}%                                        % the indent
  {-10pt \@plus -1pt \@minus -1pt}%             % the beforeskip
  {4pt \@plus 1pt}%                             % the afterskip
  {\bfseries\Large}}%                           % the style
\renewcommand{\subsection}{\@startsection
  {subsection}%                                 % the name
  {2}%                                          % the level
  {0mm}%                                        % the indent
  {-5pt \@plus -1pt \@minus -1pt}%              % the beforeskip
  {2pt \@plus 1pt}%                             % the afterskip
  {\bfseries\large}}%                      % the style
\renewcommand{\subsubsection}{\@startsection
  {subsubsection}%                              % the name
  {3}%                                          % the level
  {0mm}%                                        % the indent
  {-5pt \@plus -1pt \@minus -1pt}%              % the beforeskip
  {2pt \@plus 1pt}%                             % the afterskip
  {\bfseries\normalsize}}%                      % the style

%------------------------------------------------------------
%  TOC section name
%------------------------------------------------------------
\renewcommand\contentsname{Table of Contents}

\newcommand{\gwptop}[1]{\multicolumn{1}{|l|}{\textbf{#1}}}
\newcommand{\gwpmid}[1]{\multicolumn{1}{|l|}{#1}}
\newcommand{\gwplow}[1]{\multicolumn{1}{|r|}{#1}}

\makeatother

% \renewcommand{\cite}{\citep}
\newcommand{\byte}{b}

%-----------------------------------------------------------------------------
%-----------------------------------------------------------------------------
%   Below is some GAIA heritage stuff 
%-----------------------------------------------------------------------------
%-----------------------------------------------------------------------------
%   Macros for dealing with requirements
%-----------------------------------------------------------------------------
\makeatletter
\nplpadding{3}
\newcounter{areqi}
\renewcommand{\theareqi}{\numprint{\arabic{areqi}}}
\def\p@areq#1{\csname reqtype\endcsname-}

% default increment for requirement counter
\providecommand{\setreqincr}[1]{\setcounter{@dfreqincr}{#1}}
\newcounter{@dfreqincr}
\setcounter{@dfreqincr}{20}

\newcounter{reqincr}
\setcounter{reqincr}{\value{@dfreqincr}}

\providecommand{\newreqtype}[1]{\def\reqtype{#1}\setcounter{areqi}{0}}

\newcounter{@reqdepth}\setcounter{@reqdepth}{0}
\newenvironment{reqblock}[2][\value{@dfreqincr}]{%
\newreqtype{#2}\setcounter{reqincr}{#1}%
\addtocounter{@reqdepth}{1}}{%
\setcounter{reqincr}{\value{@dfreqincr}}%
\addtocounter{@reqdepth}{-1}}

%
%   Requirement prefix
%
\newcommand{\reqprefix}{}
\newcommand{\setReqPrefix}[1]{\renewcommand{\reqprefix}{#1}}

%
%  requirement macro
%
\providecommand{\req}[7][@noparent@]{%
\addtocounter{areqi}{\value{reqincr}}%
\protected@edef\@currentlabel{\csname p@areq\endcsname-\theareqi}%
\begin{tabular}{|%
p{0\textwidth}% dummy
>{\bfseries}p{.4\textwidth}|% Req identifier
p{.11\textwidth}|% Version
%p{.11\textwidth}|% Priority
p{.22\textwidth}|% Verification
p{.11\textwidth}|% Status
}\hline%
&\csname p@areq\endcsname -\theareqi & %
 #2 &  #5 & #6\\\hline
\ifthenelse{\equal{@noparent@}{#1}}
    {& \multicolumn{4}{p{.95\textwidth}|}{#7}\\\hline}%
    {& \multicolumn{4}{p{.95\textwidth}|}{#7}\\\hline%
& \multicolumn{4}{p{.95\textwidth}|}{Parent: #1}\\\hline}%
\end{tabular}
\\[4mm]%
\typeout{REQ:\reqprefix\csname p@areq\endcsname-\arabic{areqi},#2,#1,#6,#5}%
}

%
%   B. FREZOULS 01/13/2012
%	Applicable requirement macro
%	Created from the req command with an extra argument (the last one) 
% 	used to indicate to which system the req. is applicable
%	Display this argument in the requirement nomenclature 
% 	and add it in the log file so that the makeReqList script can add it in the Requirements.csv file
%
\providecommand{\reqapp}[8][@noparent@]{%
\addtocounter{areqi}{\value{reqincr}}%
\protected@edef\@currentlabel{\csname p@areq\endcsname-\theareqi}%
\begin{tabular}{|%
p{0\textwidth}% dummy
>{\bfseries}p{.4\textwidth}|% Req identifier
p{.07\textwidth}|% Version
%p{.11\textwidth}|% Priority
p{.07\textwidth}|% Verification
p{.11\textwidth}|% Status
p{.19\textwidth}|% Applicability
}\hline%
&\csname p@areq\endcsname -\theareqi & %
 #2 &  #5 & #6 & #7\\\hline
\ifthenelse{\equal{@noparent@}{#1}}
    {& \multicolumn{5}{p{.95\textwidth}|}{#8}\\\hline}%
    {& \multicolumn{5}{p{.95\textwidth}|}{#8}\\\hline%
& \multicolumn{5}{p{.95\textwidth}|}{Parent: #1}\\\hline}%
\end{tabular}
\\[4mm]%
\typeout{REQ:\reqprefix\csname p@areq\endcsname-\arabic{areqi},#2,#1,#6,#5,#7}%
}

%   B. FREZOULS 01/18/2012
%	Deleted requirement macro
%	Created from the req command
% 	used to 'create' deleted requirement.
% 	The requirement is not displayed in the PDF produced but it exists i.e. it is listed 
% 	in the Requirements.csv file produced by the makeReqList.rb.
%	This requirement does not 'break' the numbering schema i.e. the requirements following the requirement
%	deleted keep their number/name 
%
\providecommand{\reqdel}[7][@noparent@]{%
\addtocounter{areqi}{\value{reqincr}}%
%\protected@edef\@currentlabel{\csname p@areq\endcsname-\theareqi}%
\typeout{REQ:\reqprefix\csname p@areq\endcsname-\arabic{areqi},#2,#1,#6,#5}%
}

%   B. FREZOULS 01/18/2012
%	Deleted requirement macro
%	Created from the reqapp command
% 	used to 'create' deleted requirement.
% 	The requirement is not displayed in the PDF produced but it exists i.e. it is listed 
% 	in the Requirements.csv file produced by the makeReqList.rb.
%	This requirement does not 'break' the numbering schema i.e. the requirements following the requirement
%	deleted keep their number/name 
%
\providecommand{\reqdel}[8][@noparent@]{%
\addtocounter{areqi}{\value{reqincr}}%
\protected@edef\@currentlabel{\csname p@areq\endcsname-\theareqi}%
\typeout{REQ:\reqprefix\csname p@areq\endcsname-\arabic{areqi},#2,#1,#6,#5,#7}%
}


\def\defsavectr#1#2#3{%
  \expandafter\edef\csname#1#2\endcsname{#3}%
}
\newcounter{@checkreq}
\newenvironment{reqinsert}[2][\value{@dfreqincr}]{\mbox{}%
\defsavectr{@savectr}{\romannumeral\value{@reqdepth}}{\arabic{areqi}}%
\defsavectr{@saveinc}{\romannumeral\value{@reqdepth}}{\thereqincr}%
\addtocounter{@reqdepth}{1}%
\setcounter{reqincr}{#1}%
}{%
\addtocounter{@reqdepth}{-1}%
\setcounter{reqincr}{\csname @saveinc\romannumeral\the@reqdepth\endcsname}%
\setcounter{@checkreq}{\csname @savectr\romannumeral\the@reqdepth\endcsname+\value{reqincr}}%
\ifthenelse{\value{@checkreq}<\value{areqi}}{\errmessage{Requirement numbering incorrect: \the@checkreq<\arabic{areqi}}}{}%
\setcounter{areqi}{\csname @savectr\romannumeral\the@reqdepth\endcsname}}
\makeatother

%
%   requirement status labels
%
\providecommand{\reqiss}{Issued} % Issued requirements
\providecommand{\reqobs}{Obsolete} % Obsolete requirements
\providecommand{\reqdel}{Deleted} % Deleted requirements

% -----------------------------------------------------------------------------
% Meeting action management
% -----------------------------------------------------------------------------
\makeatletter
\newcommand{\actprefix}{}
\newcommand{\setActionItemPrefix}[1]{\renewcommand{\actprefix}{#1}}

\newcounter{aacti}
\setcounter{aacti}{0}
\renewcommand{\theaacti}{\nplpadding{2}\numprint{\arabic{aacti}}}

\newboolean{@actstarted}
\setboolean{@actstarted}{false}
\newboolean{@oldactstarted}
\setboolean{@oldactstarted}{false}


% AI in the margin
\newcommand\marginlabel[1]{\mbox{}\marginpar{\raggedright\hspace{0pt}#1}}

% the actual action macro
% altered DWE 19/6/2008 to introduce \oldaction and \nolabelaction
%   also added hyperlinks between the actions and the action table
\def\p@aact#1{\csname actprefix\endcsname}
\providecommand{\action}[3]{
\protected@edef\@currentlabel{\csname p@aact\endcsname-\theaacti}%
\ifthenelse{\boolean{@actstarted}}{\relax}{\immediate\openout7=actions\setboolean{@actstarted}{true}}
\addtocounter{aacti}{1}
\immediate\write7{\noexpand\hypertarget{\actprefix\arabic{aacti}}{\actprefix\arabic{aacti}} &
        #1 & #2 & #3\string\\\noexpand\hline}

%\vspace{-1\textheight} % does not work
\vspace{-28pt}\marginlabel{AI \hyperlink{\actprefix\arabic{aacti}}{\actprefix\arabic{aacti}}}%

\typeout{AI:\actprefix\arabic{aacti},#1,#2,#3}%
}

% the actual nolabelaction macro
\def\p@aact#1{\csname actprefix\endcsname}
\providecommand{\nolabelaction}[3]{
\protected@edef\@currentlabel{\csname p@aact\endcsname-\theaacti}%
\ifthenelse{\boolean{@actstarted}}{\relax}{\immediate\openout7=actions\setboolean{@actstarted}{true}}
\addtocounter{aacti}{1}
\immediate\write7{\actprefix\arabic{aacti} & #1 & #2 & #3\string\\\noexpand\hline}
\typeout{AI:\actprefix\arabic{aacti},#1,#2,#3}%
}

% the actual oldaction macro
\def\p@aact#1{\csname actprefix\endcsname}
\providecommand{\oldaction}[4]{
\protected@edef\@currentlabel{\csname p@aact\endcsname-\theaacti}%
\ifthenelse{\boolean{@oldactstarted}}{\relax}{\immediate\openout8=oldactions\setboolean{@oldactstarted}{true}}
\immediate\write8{\noexpand\hypertarget{#1}{#1} & #2 & #3 & #4\string\\\noexpand\hline}
\marginlabel{AI \hyperlink{#1}{#1}}%
\typeout{AI:#1,#2,#3,#4}%
}

% Parameterized the widths of the action table in case tweaking is needed.
% DWE 3/12/08

\newcommand{\actionActionNumberWidth}{.11\textwidth}
\newcommand{\actionActioneeWidth}{.12\textwidth}
\newcommand{\actionActionDateWidth}{.12\textwidth}
\newcommand{\actionActionDescriptionWidth}{.56\textwidth}

% outputs the list of actions if any are defined
\providecommand{\listofactions}{%
\IfFileExists{actions}{%
\immediate\closeout7
\immediate\closeout8
\newcounter{actli}
\setcounter{actli}{1}
\newcommand{\countact}{\nplpadding{2}\numprint{\arabic{actli}}\addtocounter{actli}{1}}
\begin{longtable}{|p{\actionActionNumberWidth}|>{\raggedright}p{\actionActioneeWidth}|>
{\raggedright}p{\actionActionDateWidth}|p{\actionActionDescriptionWidth}|}
\hline
Id & Actionee & Due Date & Action\\\hline
\IfFileExists{oldactions}{\input{oldactions}}{}
\input{actions}
\end{longtable}
}{%
No actions have been identified.}
}

% -----------------------------------------------------------------------------
% Useful definition
% -----------------------------------------------------------------------------
\def\aaps{A\&AS}           % Astronomy and Astrophysics Suplement
\def\aap{A\&A}             % Astronomy and Astrophysics
\def\ssr{Space~Sci.~Rev.}  % Space Science Reviews
\def\apj{ApJ}              % Astrophysical Journal
\def\aj{AJ}                % Astronomical Journal
\def\mnras{MNRAS}          % Monthly Notices of the RAS
\def\araa{ARA\&A}          % Annual Review of Astron and Astrophys
\def\nat{Nature}           % Nature
\def\apjl{ApJ}             % Astrophysical Journal, Letters

\def\degr{\hbox{$^\circ$}} 
\def\arcmin{\hbox{$^\prime$}}
\def\arcsec{\hbox{$^{\prime\prime}$}}
\def\fs{\hbox{$.\!\!^{\rm s}$}}
\def\fdg{\hbox{$.\!\!^\circ$}}
\def\farcm{\hbox{$.\mkern-4mu^\prime$}}
\def\farcs{\hbox{$.\!\!^{\prime\prime}$}}
\def\sun{\hbox{$\odot$}}

%
% this makes list spacing single spaced.
%
\newenvironment{enumerate_single}{
\begin{enumerate}
  \setlength{\itemsep}{1pt}
  \setlength{\parskip}{0pt}
  \setlength{\parsep}{0pt}}
{\end{enumerate}
}
\newenvironment{itemize_single}{
\begin{itemize}
  \setlength{\itemsep}{1pt}
  \setlength{\parskip}{0pt}
  \setlength{\parsep}{0pt}}
{\end{itemize}
}

%
%   convenience macros
%
\providecommand{\pu}[2]{\ensuremath{#1\,\mbox{#2}}}
\providecommand{\secs}[1]{\pu{#1}{s}}
\providecommand{\uas}[1]{\pu{#1}{$\mu$as}}
\providecommand{\muas}[1]{\pu{#1}{$\mu$as}}
\providecommand{\muasonly}{\ensuremath{\mu\mbox{as}}}
\providecommand{\inp}[1]{{\tt #1}}
\providecommand{\prog}[1]{{\it #1}}
\providecommand{\secref}[1]{Section~\ref{#1}}
\providecommand{\appref}[1]{Appendix~\ref{#1}}
\providecommand{\partref}[1]{Part~\ref{#1}}
\providecommand{\tabref}[1]{Table~\ref{#1}}
\providecommand{\figref}[1]{Figure~\ref{#1}}
\providecommand{\eqnref}[1]{Eq.~\ref{#1}}
\providecommand{\reqref}[1]{Req.~\ref{#1}}
\providecommand{\actref}[1]{AI~\ref{#1}}
\providecommand{\class}[1]{{\it #1}}
\providecommand{\pack}[1]{{\em #1}}
\providecommand{\property}[1]{{\em #1}}
\providecommand{\method}[1]{{\em #1}}
\providecommand{\file}[1]{{\em #1}}
\providecommand{\directory}[1]{{\em #1}}
\providecommand{\code}[1]{{\tt #1}}

% new bib
\newcommand{\citell}{\citeyear}
\newcommand{\citellp}{\citeyearpar}

\renewcommand{\vec}[1]{\ensuremath{\mathchoice{\mbox{\boldmath$\displaystyle#1$}}
{\mbox{\boldmath$\textstyle#1$}}
{\mbox{\boldmath$\scriptstyle#1$}}
{\mbox{\boldmath$\scriptscriptstyle#1$}}}}

%------------------ caption format ----------------------------
% added by LL to get nicer captions to tables and figures
% makecaption redefined (small, FIGURE in sc, 0.9\hsize):
\setlength\abovecaptionskip{10\p@}
\setlength\belowcaptionskip{0\p@}
\long\def\@makecaption#1#2{%
  \vskip\abovecaptionskip
  \sbox\@tempboxa{\small {\sc #1:} #2}%
  \ifdim \wd\@tempboxa >0.9\hsize
    \hb@xt@\hsize{\hfil\parbox{0.9\hsize}{\small {\sc #1:} #2}\hfil} %\par
  \else
    \global \@minipagefalse
    \hb@xt@\hsize{\hfil\box\@tempboxa\hfil}%
  \fi
  \vskip\belowcaptionskip}
%------------------ end caption format ----------------------------

%----------------- Paragraph numbering - JSH

% put \npara at the start of each paragraph or \item you want to be numbered

\newcounter{@dfparincr}
\setcounter{@dfparincr}{5}

\newcounter{gaiapar}
\providecommand{\thegaiapar}{\numprint{\arabic{gaiapar}}}
\providecommand{\npara}{
\addtocounter{gaiapar}{\value{nparaincr}}
\marginlabel{\S\thegaiapar}}

% default increment for requirement counter
\providecommand{\setnparaincr}[1]{\setcounter{@dfparincr}{#1}}
\newcounter{nparaincr}
\setcounter{nparaincr}{\value{@dfparincr}}

%-----------------------
%
% Usefull stuf from Wruter2Latex
%
\newcommand\textsubscript[1]{\ensuremath{{}_{\text{#1}}}}
