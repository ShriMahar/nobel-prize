import streamlit as st 
import pandas as pd
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from PIL import Image
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from os import path
import nltk
nltk.download('stopwords')

# custom stop words for wordcloud
def stop_words():
    # create some custom stop words
    custom_stop_words = {'discovery', 'writing','discoveries', 'international','work', 'development', 'contribution','contributions', 'his', 'pioneering', 'recognition',
                    'concerning', 'determination', 'mechanisms','economic', 'chemistry', 'chemical', 'theory', 'analysis',
                    'studies', 'invention', 'structure','effect','research', 'method', 'especially', 'investigation', 'high', 'use', 'fundamental', 'peace',
                    'physics', 'researches', 'field', 'empirical','new', 'methods', 'relating', 'particular', 'particularly', 'time', 'great', 'effort',
                    'mechanism', 'investigations','important', 'system', 'called', 'analyses', 'design', 'economics', 'regarding', 'principle',
                    'role', 'laid', 'works', 'connection', 'rendered'}
    default_stop_words = set(stopwords.words('english'))

    # Combine default and custom stop words
    all_stop_words = default_stop_words.union(custom_stop_words)
    
    return all_stop_words

# ***** Title******
title = f'<span style="font-size: 32px; text-align:center; color:#746969; font-weight: bold;">{"Decoding Excellence :medal:"}</span>'
st.markdown(title, unsafe_allow_html=True)

#***********sub heading**********
styled_text = f'<span style="font-size: 22px; color:#fc8300; font-weight: bold;">{"A Data Analysis of Nobel Laureates"}</span>'
st.markdown(styled_text, unsafe_allow_html=True)


# *******reading the dataframe*******
df = pd.read_csv("data/nobel_laureates.xls")
org_df = pd.read_csv("data/organisations.xls")


# ******* helper functions *********
def change_label_style(label, font_size='18px', font_color='#746969', font_family='sans-serif'):
    html = f"""
    <script>
        var elems = window.parent.document.querySelectorAll('p');
        var elem = Array.from(elems).find(x => x.innerText == '{label}');
        elem.style.fontSize = '{font_size}';
        elem.style.color = '{font_color}';
        elem.style.fontFamily = '{font_family}';
    </script>
    """
    st.components.v1.html(html)

def ColourWidgetText(wgt_txt, wch_colour = '#000000'):
    htmlstr = """<script>var elements = window.parent.document.querySelectorAll('*'), i;
                    for (i = 0; i < elements.length; ++i) { if (elements[i].innerText == |wgt_txt|) 
                        elements[i].style.color = ' """ + wch_colour + """ '; } </script>  """

    htmlstr = htmlstr.replace('|wgt_txt|', "'" + wgt_txt + "'")
    components.html(f"{htmlstr}", height=1, width=0)
    
    
# *******sidebar********    
st.sidebar.image("https://th-thumbnailer.cdn-si-edu.com/ZEFdV0G1v_ytsehbUnr2HlpvfsQ=/fit-in/1600x0/filters:focal(515x296:516x297)/https://tf-cmsv2-smithsonianmag-media.s3.amazonaws.com/filer/40/8a/408acbae-404f-4f17-8e49-b3099699e1d6/efkeyb-wr.jpg", use_column_width=True)    
selected_radio = st.sidebar.radio(
    "Select field to learn more..",
    ["All", "Physics", "Chemistry", "Literature", "Medicine", "Economics", "Peace", "Peace (Organisations)"])
     

#*******Intro paragraph*******
custom_purple_scale = ['#746969', '#66a9c2', '#249fcd', '#ff9b2f', '#fc8300', '#ffd92f']

text = """
    <p style='text-align: justify;'>
    The Nobel Prize is a set of prestigious international awards given annually in several categories, recognizing outstanding achievements in various fields. The prizes were established by the will of Alfred Nobel, a Swedish inventor, scientist, and philanthropist, in 1895. The Prizes are awarded for exceptional contributions in the fields of Physics, Chemistry, Medicine, Literature, Peace, and Economic Sciences and were first awarded in the year 1901.
    <p style='text-align: justify;'>
    Analyzing the Nobel laureates data allows us to celebrate and understand the achievements of outstanding individuals and organizations.  The Nobel Prize has a rich history dating back to 1901. Analyzing the data provides insights into historical events, societal changes, and global trends over the years. Examining demographic data among Nobel laureates sheds light on gender and geographical representation, fostering discussions about diversity and inclusivity in various fields.
    </p></p>
    """
st.markdown(text, unsafe_allow_html=True)


# ********* facts ***********
label = "<b>Number of winners between 1901 and 2023 : 1000 Awardees (includes people and organisations)</b>"
custom_style = "color: #746969; font-size: 18px;"
st.markdown(f'<p style="{custom_style}">{label}</p>',unsafe_allow_html=True)

#*********metrics************
col1, col2 = st.columns(2)
col1.metric("Overall Avg Age of Women", value = "58 years")
ColourWidgetText('Overall Avg Age of Women', '#249fcd') 

col2.metric("Overall Avg Age of Men", value = "60 years")
ColourWidgetText('Overall Avg Age of Men', '#249fcd')  

# repeat laureates
st.markdown(" *** ")
repeat = f'<span style="font-size:22px; color:#fc8300; font-weight: bold;"><br><br><br>{" Did anyone snag the Nobel Prize more than once? 🏆🤔 ?"}</span>'           
st.markdown(repeat, unsafe_allow_html=True)

repeat_laureates = df[df.duplicated(subset=['firstname', 'surname'], keep=False)]

#******** DATA FILTERING******

# wordcloud
research_topic = df[['firstname','category', 'motivation', 'year_of_award']].copy()
result = research_topic.groupby('category')['motivation'].apply(lambda x: ' '.join(x)).reset_index()

# countries
recipient_countries = df.groupby(['country_of_birth'])['country_of_birth'].count().reset_index(name="count")

# gender ratio in each category
gen_cat = df.groupby(['category', 'gender']).size().reset_index(name="count")
filtered_data = gen_cat[gen_cat['category'] == selected_radio]
colours = {'male':'#66a9c2','female': '#fc8300' }

# 2 times winners
repeat_laureates = df[df.duplicated(subset=['firstname', 'surname'], keep=False)]
header = dict(values=list(repeat_laureates[['firstname', 'surname', 'category']].columns),
              fill_color = '#249fcd',
              font=dict(color='#FFFFFF'))
cells = dict(values = [repeat_laureates['firstname'], repeat_laureates['surname'], 
                       repeat_laureates['category']],
              align = 'left')

repeatwinners = go.Figure(data=[go.Table(header=header, cells = cells)])
repeatwinners.update_layout(title_text='Double-dippers of the prestigious prize!',
                   width=600,
                   height=410)
st.plotly_chart(repeatwinners)

# award sharing
sharing_cat = df.groupby(['category','award_shared_with']).size().reset_index(name = "count")

#*********** text for charts ************
all_text1 = """
<p style='text-align: justify;'>
On an average, the age of Nobel Prize winners has demonstrated an upward trend over the years. While both Physicist and Chemists were making their ground breaking discoveries while they were young since the inception of Nobel Prize awards, where the average age of the recipient was roughly <b> 50 years </b> in the first decade (1901 - 1910) while it has jumped to <b> > 65 </b> for Chemistry and Physics in the last decade (2010 - 2019). 
<p style='text-align: justify;'>
This could be because a century ago, there were perhaps only 1000s of physicists, compared to an estimated millions of them today. The surge in the overall number of breakthroughs each year might be surpassing the capacity of awards to keep pace with the deserving individuals hence a longer waiting time.
<p style='text-align: justify;'>
On the otherhand It is interesting to note that  the declining age profile of peace prize winners over the decades.
</p></p></p>
"""
     
all_text2 = """
            <p style='text-align: justify;'>
            From 1901 to 2023, <b>women</b> have been honored with the Nobel Prize on <b>65 times</b> comapred to <b>men</b> who were awarded the prize <b>905 times</b>.    
            <p style='text-align: justify;'>
             There is a significant gender disparity and historically majority of the Nobel laureates have been male especially in field of Science (Physics and Chemistry in particularly) and Economics where less than five percent of all winners have been female.
            <p style='text-align: justify;'>
             On a historical context, Nobel prizes were established in the late 19th century when opportunities for women to pursue advanced education and careers in science and academia were very limited. This under representation have had a ripple effect on the prospective pool of future Nobel laureates.
            <p style='text-align: justify;'>
            The years <b> 2009 , 2018, 2020 and 2023 </b> (4 recipients) have been the banner years for women at the Nobel Prize with maximum representaion of women by far with four awardees in 2018, 2020, and 2023, and five recipients in the year 2009.Its essential to note that advancements in gender equality are ongoing.
            </p></p></p>
            """
             
all_text3 = """ 
            <br>
            <p style='text-align: justify;'>
            From 1901 to 2023, the field of Medicine has received the highest number of Nobel Prizes, having been awarded 227 times. 
            Following closely are Physics with 225 awards and Chemistry with 220 awards.</p>
            """     
            
all_text4 = """ 
<p style='text-align: justify;'>
Analyzing institutions producing Nobel laureates provides valuable insights into the academic landscape, fosters a culture of excellence, and contributes to advancements in science, literature, and other fields. 
<p style='text-align: justify;'>
The continents of <b> North America (USA in particular) and Europe </b> are home to the majority of institutions that produce Nobel laureates.
<p style='text-align: justify;'>
One of the notable indicators of a university's prestige is its count of Nobel Prize laureates among its faculty or alumni. If you aspire to receive a Nobel Prize in the future, you may consider applying to the aforementioned universities. Who knows? Perhaps one day, your name will join the ranks of distinguished laureates associated with these institutions! :)
</p></p></p>
"""

all_text5 = """   
<p style='text-align: justify;'>
The <b>United States</b> takes a prominent position in Nobel Prize achievements in terms of place of birth of the awardee. USA has the highest number (292 individuals) laureates born in this country,  The United Kingdom ranks second in the list with 106 winners. followed by Germany with 85 indviduals.
<p style='text-align: justify;'>
<b>Note:</b> The data doesn't include the citizenship of the candidate, some candidates moved across the world to find a position where they could do their breakthrough work. Therefore the geographical distribution of nobel laureates is based on their place of birth.
</p></p>
"""

all_text6 = """   
<p style='text-align: justify;'>
In 1901 all the winners were European. European countries were home to most prize-producing institutions 
before the World War II (1939 - 1945), after which the US makes a stunning debut, taking a lead by winning
more 290 nobel prizes, exceeding any other country, by a wide margin. This number is based on the place of 
birth of the awardee, if we were to consider the institution the awardee was affliated at the time of 
winning the prize, the number of prizes won by USA alone would be much higher.
</p>
"""

all_text7 = """
<p style='text-align: justify;'>
The age of Nobel Prize laureates has sparked considerable interest and debate. Although there is no rigid criterion specifying the age at which groundbreaking contributions must occur, historical patterns indicate that numerous laureates have made substantial achievements early in their careers. . 

<p style='text-align: justify;'>
Nevertheless, exceptions exist, with certain laureates gaining recognition much later in life for enduring contributions or discoveries made over an extended period. Ultimately, age stands as just one factor among many.

The above 2 tables shows the list of top 3 youngest and oldest individuals to receive the prestigious award. After all age is just a number! 
"""
#**************************************************************************************************************************************************      
            
# Function to display content based on radio button selection
def display_content(selected_radio):
    if selected_radio == 'All':
        # You selected Option 1
        container = st.container()
       
        row1_1, row1_space2, row1_2 = container.columns(( 1, 0.1, 0.1))
        row2_1, row2_space2, row2_2 = container.columns(( 1, 0.1, 0.1))
        row3_1, row3_space2, row3_2 = container.columns(( 1, 1, 1))
        row4_1, row4_space2, row4_2 = container.columns(( 1, 0.1, 0.1))
        row5_1, row5_space2, row5_2 = container.columns(( 1, 0.1, 0.1))
        row6_1, row6_space2, row6_2 = container.columns(( 1, 0.1, 0.1))
        row7_1, row7_space2, row7_2 = container.columns(( 1, 1, 1))
        row8_1, row8_space2, row8_2 = container.columns(( 1, 1, 1))
        row9_1, row9_space2, row9_2 = container.columns(( 1, 0.01, 0.01))
        row10_1, row10_space2, row10_2 = container.columns(( 1, 0.1, 0.1))
        row11_1, row11_space2, row11_2 = container.columns(( 1, 1, 1))
        row12_1, row12_space2, row12_2 = container.columns(( 1, 0.01, 0.01))



        with row1_1:

            # average age analysis
            avg_age = df.groupby(['period', 'category'])['awarded_age'].mean().reset_index()
            age = f'<span style="font-size:22px; color:#fc8300; font-weight: bold;">{"Trends in Age of Nobel Prize Laureates :chart_with_upwards_trend:"}</span>'
            st.markdown(age, unsafe_allow_html=True)

            fig = px.line(avg_age, x="period", y="awarded_age", color='category', 
                          orientation='h',      
                          height=400,
                          width = 800,
                          title="Trending Ages of Nobel Laureates Over Decades",
                          color_discrete_map={'Chemistry':'#0000FF',
                                              'Physics': '#E0B0FF', 
                                              'Economics':'#249fcd', 
                                              'Peace':'#008000', 
                                              'Medicine':'#fc8300', 
                                              'Literature':'#ffd92f'})

            st.markdown(all_text1, unsafe_allow_html=True)
            st.plotly_chart(fig)

            # gender analysis
            gender = f'<span style="font-size:22px; color:#fc8300; font-weight: bold;"><br><br>{"The Scarcity of Female Laureates :female-scientist:"}</span>'
            st.markdown(gender, unsafe_allow_html=True)
            
            fig1 = px.bar(gen_cat, x="count", y="category", color='gender', orientation='h',      
                          height=400,
                          title="The Nobel Prize Gender Gap",
                          hover_data={"category": False, 
                                      "gender": False,
                                      "count" : True},
                          hover_name="gender",
                          labels={'count': 'No.of recipients',
                                  'category': 'Category'},
                          color_discrete_map=colours)
            
            st.plotly_chart(fig1)
            
            gender_ratio = df['gender'].value_counts().reset_index(name="count")
            fig4 = px.bar(gender_ratio, y="gender", x="count", 
                          orientation='h',
                          title="Total Number of Male and Female Nobel Prize Recipients (Until 2023)",
                          color_discrete_sequence=["#249fcd"])
            fig4.update_layout(
                autosize=False,
                height=400,
                yaxis_title='Gender',
                xaxis_title='No of Awards'
            )
            st.plotly_chart(fig4)          
            st.markdown(all_text2, unsafe_allow_html=True)
  
            
        with row2_1:
            
             fieldInst = f'<span style="font-size:22px; color:#fc8300; font-weight: bold;"><br><br>{"Distribution of Awards Across Fields & Institutions :microscope: :classical_building:"}</span>'
             st.markdown(fieldInst, unsafe_allow_html=True)
   
        
        # category analysis    
        with row3_1:

            custom_purple_scale = ['#746969', '#66a9c2', '#249fcd', '#ff9b2f', '#fc8300', '#ffd92f']
            awards_per_category = df['category'].value_counts().reset_index(name="count")
            fig2 = px.pie(awards_per_category, names='category', values='count', 
                          title='Percentage of Awards Won in Each Field',
                          color_discrete_sequence = custom_purple_scale)
                          
            fig2.update_layout(
                autosize=False,
                width=400,
                height=400
            )
            st.plotly_chart(fig2)
            
        with row3_2:     
             st.markdown(all_text3, unsafe_allow_html=True)
        
        
        # institution analysis    
        with row4_1:
            
            institute = df['Institute'].value_counts().head(20).reset_index(name="count")
            
            fig3 = px.bar(institute, x="Institute", y="count",  
                          title="Institution With Most Nobel Prize Recipients",
                          color_discrete_sequence=["#249fcd"])
            fig3.update_layout(
                autosize=False,
                #height=800,
                xaxis_tickangle=-45,
                xaxis_title='University',
                yaxis_title='No of Awards'
            )
            st.plotly_chart(fig3)
 
            
        with row5_1:
            st.markdown(all_text4, unsafe_allow_html=True)
     
        
        # geographical analysis
        with row6_1:
            
            #*******Plot geographical distribution of nobel prize recipients*******
            geography = f'<span style="font-size:22px; color:#fc8300; font-weight: bold;"><br><br>{" Where do Nobel Laureates come from? :earth_africa: "}</span>'
            st.markdown(geography, unsafe_allow_html=True)
            st.markdown(all_text5, unsafe_allow_html=True)
         
            
        with row7_1:
            
            #*******Plot geographical distribution of nobel prize recipients*******          
            custom_purple_scale = ['#d3d3d3','#746969', '#66a9c2', '#249fcd', '#ff9b2f', '#fc8300', '#ffd92f']
            fig5 = px.choropleth(recipient_countries, locations='country_of_birth', 
                                color='count', 
                                hover_name='country_of_birth',
                                color_continuous_scale=custom_purple_scale, locationmode='country names', 
                                title=' Geographical Distribution of Nobel Prize Recipients',
                                labels={'count': 'Number of recipients',
                                        'country_of_birth': 'Country'})
            fig5.update_layout(
                autosize=False,
                width=800,
                height=600,
                title_x=0.1
            )
            st.plotly_chart(fig5)
            
            
        with row8_1:    
            
            top10countries = recipient_countries.sort_values(by='count', ascending=False).head(10)
            fig6 = px.bar(top10countries, x="country_of_birth", y="count",  
                          title="Top 10 countries with the highest number of Nobel laureates based on their birthplace",
                          color_discrete_sequence=["#249fcd"])
            fig6.update_layout(
                autosize=False,
                width=750,
                height=500,
                xaxis_tickangle=-45,
                title_x=0.1,
                xaxis_title='Countries',
                yaxis_title='No of Awards'
            )
            st.plotly_chart(fig6)
            
            
        # dominance of usa    
        with row9_1:    
            
            usa = f'<span style="font-size:22px; color:#fc8300; font-weight: bold;"><br><br><br>{" When did the USA start to dominate the Nobel Prize charts?"}</span>'           
            st.markdown(usa, unsafe_allow_html=True)
            st.markdown(all_text6, unsafe_allow_html=True)
            
            top5countries = df[df['country_of_birth'].isin(["USA", "United Kingdom", "Germany", "France", "Sweden"])]
            usa_dominance = top5countries.groupby(['country_of_birth', 'period']).size().reset_index(name = "count")
            usa_dominance['cumsum'] =  usa_dominance.groupby(['country_of_birth'])['count'].cumsum()
            
            fig7 = px.line(usa_dominance, x="period", y="cumsum", color='country_of_birth', 
                           title='Dominance of USA in Nobel Prize Acheivement',
                           color_discrete_sequence= px.colors.qualitative.Bold)
            fig7.update_layout(
                autosize=False,
                width=900,
                height=600,
                xaxis_tickangle=-45,
                title_x=0.1,
                xaxis_title='Countries',
                yaxis_title='No of Awards'
            )
            st.plotly_chart(fig7)
            
            
        with row10_1:    
            
            yo_ol = f'<span style="font-size:22px; color:#fc8300; font-weight: bold;"><br><br><br>{" How Old Are the Youngest and Oldest Laureates ?:woman::older_man:"}</span>'           
            st.markdown(yo_ol, unsafe_allow_html=True)
            
            
        # youngest and oldest laureates    
        with row11_1:

            youngest = df.sort_values(by='awarded_age').head(3)
            header = dict(values=list(youngest[['firstname', 'surname', 'category', 'awarded_age']].columns),
                          fill_color = '#249fcd',
                          font=dict(color='#FFFFFF'))
            cells = dict(values = [youngest['firstname'], youngest['surname'], 
                                   youngest['category'], youngest['awarded_age']],
                          align = 'left')
            
            fig7 = go.Figure(data=[go.Table(header=header, cells = cells)])
            fig7.update_layout(title_text='3 Youngest Nobel Laureates..',
                               width=400,
                               height=300)
            st.plotly_chart(fig7)
            
        with row11_2:
            
            oldest = df.sort_values(by='awarded_age').tail(3)
            header = dict(values=list(oldest[['firstname', 'surname', 'category', 'awarded_age']].columns),
                          fill_color = '#249fcd',
                          font=dict(color='#FFFFFF'))
            cells = dict(values = [oldest['firstname'], oldest['surname'], 
                                   oldest['category'], oldest['awarded_age']],
                          align = 'left')
            
            fig8 = go.Figure(data=[go.Table(header=header, cells = cells)])
            fig8.update_layout(title_text='3 Oldest Nobel Laureates..',
                               width=400,
                               height=300)
            st.plotly_chart(fig8)
            
            
        with row12_1:
            
            st.markdown(all_text7, unsafe_allow_html=True)

             
#************* end of option 'All'******************
    
    # PHYSICS    
    elif selected_radio == 'Physics':
        
        # award shared in physics
        filtered_physics = sharing_cat[sharing_cat['category'] == 'Physics'].copy()
        collab_list=["Individual", "2 laureates", "3 laureates", "4 laureates"] 
        filtered_physics['awarded_to'] = collab_list
        filtered_physics.drop(['award_shared_with'], axis=1, inplace=True)
        custom_purple_scale = ['#746969', '#249fcd', '#ff9b2f', '#fc8300', '#ffd92f']
        fig = px.pie(filtered_physics, values='count', names='awarded_to', title='Nobel Prize Jointly Awarded to Individual/Contributors for Physics',
                    color_discrete_sequence = custom_purple_scale)
        hover_template = "<b>%{label}</b><br>Value: %{value}"
        fig.update_traces(hovertemplate=hover_template)
        st.plotly_chart(fig)
        st.markdown("""
                    **It appears that the majority of physics prizes were bestowed upon collaborative work involving two individuals**  \n
                    47 physics prizes have been given to one laureate only.  
                    84 individuals have shared the Nobel Prize with 1 other laureate.  
                    54 individuals have shared the Nobel Prize with 2 other laureate.  
                    40 individuals have shared the Nobel Prize with 3 other laureate.  
                    
                    **Reason for this?**   
                    statutes of the Nobel Foundation, it is stipulated: "A prize amount may be equally divided between two works, each deemed deserving of recognition. If a rewarded work has been collaboratively produced by two or three individuals, the prize shall be jointly awarded to them. Under no circumstances may a prize amount be divided among more than three persons."
                    """)
        st.text("")
        st.text("")
        st.markdown("***")
        
        # gender disparity in physics
        fig9 = px.bar(filtered_data, x="count", y="gender", color='gender', orientation='h',      
                     height=400,
                     title='How many female physicists have won the nobel so far?',
                     hover_data={"category": False, 
                                 "gender": False,
                                 "count" : True},
                     hover_name="gender",
                     labels={'count': 'No.of recipients',
                             'gender': 'Gender'},
                     color_discrete_map=colours)
        st.plotly_chart(fig9)
        st.markdown("The fields of physics and astronomy have a long history of being male-dominated. A total of 225 people have won the Nobel Prize in physics, of which only **5 are women**. Marie Curie was the first woman to ever win the award in 1903. There was a substantial 60-year gap between the first and second women (Maria Goeppert-Mayer won in 1963) to achieve the remarkable feat of winning the Nobel Prize in Physics.   " )
        st.text("")
        st.text("")
        st.markdown("***")
        
        # WORDCLOUD
        text = result.loc[result['category'] == selected_radio, 'motivation']
        new_text = [str(x) for x in text][0]
        all_stop_words = stop_words()
        wordcloud = WordCloud(stopwords=all_stop_words,  background_color="white").generate(new_text)

        #  focus of research in physics
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.markdown("<h6 style='color:#000000;'>Top areas of research in Physics</h6>", unsafe_allow_html=True)
        st.text("")
        st.image(wordcloud.to_image(), caption='Top areas of research in physics', use_column_width=True)
        st.markdown("""
                The Nobel Prize in Physics is awarded for outstanding contributions to the field of physics. Some of the research topics that have led to Nobel Prizes in Physics include \n
                **Quantum Mechanics (e.g., 1922, 1932, 1954)** - Contributions to the development of quantum mechanics, \n
                **Particle Physics and the Standard Model (e.g., 1979, 1999, 2013)** - Discoveries related to the fundamental particles \n
                **Solid-State Physics and Semiconductors (e.g., 1956, 2000)** - Advancements in the understanding of the properties of solid materials and the development of semiconductor
                """)


    # CHEMISTRY
    elif selected_radio == 'Chemistry':
        
        # award shared in chemistry
        filtered_chemistry = sharing_cat[sharing_cat['category'] == 'Chemistry'].copy()
        collab_list=["Individual", "2 laureates", "3 laureates", "4 laureates"] 
        filtered_chemistry['awarded_to'] = collab_list
        filtered_chemistry.drop(['award_shared_with'], axis=1, inplace=True)
        custom_purple_scale = ['#746969', '#249fcd', '#ff9b2f', '#fc8300', '#ffd92f']
        fig = px.pie(filtered_chemistry, values='count', names='awarded_to', title='Nobel Prize Jointly Awarded to Individual/Contributors for Chemistry',
                    color_discrete_sequence = custom_purple_scale)
        hover_template = "<b>%{label}</b><br>Value: %{value}"
        fig.update_traces(hovertemplate=hover_template)
        st.plotly_chart(fig)
        st.markdown("""
                    **The Nobel Prize in chemistry has been awarded to a total 194 individuals between 1901 and 2023 of which:**  \n
                    63 chemistry prizes have been given to one laureate only.  
                    58 individuals have shared the Nobel Prize with 1 other laureate.  
                    57 individuals have shared the Nobel Prize with 2 other laureate.    
                    16 individuals have shared the Nobel Prize with 3 other laureate.  
                    
                    """)
        st.text("")
        st.text("")
        st.markdown("***")
                
        
        # gender disparity in chemistry
        fig9 = px.bar(filtered_data, x="count", y="gender", color='gender', orientation='h',      
                     height=400,
                     hover_data={"category": False, 
                                 "gender": False,
                                 "count" : True},
                     hover_name="gender",
                     labels={'count': 'No.of recipients',
                             'gender': 'Gender'},
                     color_discrete_map=colours)
        st.plotly_chart(fig9)
        st.markdown("Out of the 114 Nobel Prizes awarded in Chemistry over the years, involving 189 individuals as laureates, eight women have been recipients slightly higher that Physics which stands at 5 female recipients. In most cases, these awards were shared.")
        st.text("")
        st.text("")
        st.markdown("***")
        
        # WORDCLOUD
        text = result.loc[result['category'] == selected_radio, 'motivation']
        new_text = [str(x) for x in text][0]
        all_stop_words = stop_words()
        wordcloud = WordCloud(stopwords=all_stop_words,  background_color="white").generate(new_text)

        #  focus of research in chemistry
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.markdown("<h6 style='color:#000000;'>Top areas of research in Chemistry</h6>", unsafe_allow_html=True)
        st.image(wordcloud.to_image(), caption='Chemistry', use_column_width=True)
        st.markdown(""" 
                    The Nobel Prize in Chemistry is awarded for outstanding contributions to the field of chemistry. Here are some research topics that have led to Nobel Prizes in Chemistry: \n **Chemical Synthesis (e.g., 1984, 2005)** - Recognition for the development of methods in organic synthesis, \n discovery of **new chemical elements** and \n many Nobel Prizes have been awarded for the determination of the structure of **proteins** and nucleic acids.
                    """)
        
        
        
    # LITERATURE
    elif selected_radio == 'Literature':
        
        # # award shared in literature
        filtered_literature = sharing_cat[sharing_cat['category'] == 'Literature'].copy()
        collab_list=["Individual", "2 laureates"] 
        filtered_literature['awarded_to'] = collab_list
        filtered_literature.drop(['award_shared_with'], axis=1, inplace=True)
        custom_purple_scale = ['#746969', '#249fcd', '#ff9b2f', '#fc8300', '#ffd92f']
        fig = px.pie(filtered_literature, values='count', names='awarded_to', title='Nobel Prize Jointly Awarded to Individual/Contributors for Literature',
                    color_discrete_sequence = custom_purple_scale)
        hover_template = "<b>%{label}</b><br>Value: %{value}"
        fig.update_traces(hovertemplate=hover_template)
        st.plotly_chart(fig)
        st.write(" The Nobel Prize in Literature has been awarded 116 times between the years 1901 and 2023, although 93.3%  of the time the prize has been awarded for individual work except on 4 ocassions prize in Literature has been shared between two individuals \n ")
        st.text("")
        st.text("")
        st.markdown("***")
        
        # gender disparity in literature
        fig9 = px.bar(filtered_data, x="count", y="gender", color='gender', orientation='h',      
                     height=400,
                     hover_data={"category": False, 
                                 "gender": False,
                                 "count" : True},
                     hover_name="gender",
                     labels={'count': 'No.of recipients',
                             'gender': 'Gender'},
                     color_discrete_map=colours)
        st.plotly_chart(fig9)
        st.markdown("116 Nobel Prizes in Literature have been awarded since 1901. The field  comes second with a total of 17 female laureates, following closely behind the Nobel Peace Prize which boasts of 19 female laureates in total, the highest number among all the categories.")
        st.text("")
        st.text("")
        st.markdown("***")
        
        # WORDCLOUD
        text = result.loc[result['category'] == selected_radio, 'motivation']
        new_text = [str(x) for x in text][0]
        all_stop_words = stop_words()
        wordcloud = WordCloud(stopwords=all_stop_words,  background_color="white").generate(new_text)

        #  focus in literature
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.image(wordcloud.to_image(), caption='Literature', use_column_width=True)
        st.markdown("""
                    The Nobel Prize in Literature is awarded for outstanding contributions to literature, including novels, poetry, essays, and plays. Here are some broad themes and topics that have been recognized with the Nobel Prize in Literature: \n
                    Personal narratives and autobiographical novels reflecting the author's **life** experiences. \n
                    Literature that addresses issues of **human rights**, social justice, and the struggles of marginalized communities. \n
                    **Historical Novels** - Novels that vividly depict historical events, eras, or characters, offering insights into the past. \n
                    """)
        
    
    # MEDICINE    
    elif selected_radio == 'Medicine':
        
        # award shared in medicine
        filtered_medicine	 = sharing_cat[sharing_cat['category'] == 'Medicine'].copy()
        collab_list=["Individual", "2 laureates", "3 laureates", "4 laureates"] 
        filtered_medicine	['awarded_to'] = collab_list
        filtered_medicine	.drop(['award_shared_with'], axis=1, inplace=True)
        custom_purple_scale = ['#746969', '#249fcd', '#ff9b2f', '#fc8300', '#ffd92f']
        fig = px.pie(filtered_medicine	, values='count', names='awarded_to', title='Nobel Prize Jointly Awarded to Individual/Contributors for Medicine',
                    color_discrete_sequence = custom_purple_scale)
        hover_template = "<b>%{label}</b><br>Value: %{value}"
        fig.update_traces(hovertemplate=hover_template)
        st.plotly_chart(fig)
        st.markdown("""
                    **Looks like majority of the prizes in medicine or physiology were awarded to work that has been produced by three persons.**  \n
                    40 medicine prizes have been given to one laureate only.  
                    78 individuals have shared the Nobel Prize with 1 other laureate.   
                    93 individuals have shared the Nobel Prize with 2 other laureate.    
                    16 individuals have shared the Nobel Prize with 3 other laureate.  
                    
                    **Reason for this?**   
                    statutes of the Nobel Foundation, it is stipulated: "A prize amount may be equally divided between two works, each deemed deserving of recognition. If a rewarded work has been collaboratively produced by two or three individuals, the prize shall be jointly awarded to them. Under no circumstances may a prize amount be divided among more than three persons."
                    """)
        st.text("")
        st.text("")
        st.markdown("***")

        
        # gender disparity in medicine
        fig9 = px.bar(filtered_data, x="count", y="gender", color='gender', orientation='h',      
                     height=400,
                     hover_data={"category": False, 
                                 "gender": False,
                                 "count" : True},
                     hover_name="gender",
                     labels={'count': 'No.of recipients',
                             'gender': 'Gender'},
                     color_discrete_map=colours)
        st.plotly_chart(fig9)
        st.markdown("As of 2023, Nobel Prizes have been awarded to 13 women in the field of Medicine or Physiology, as opposed to men wo were awarded the Nobel Prize 214 times. The most recent one being in 2023  to Katalin Karikó along with Drew Weissman for their discoveries that enabled the development of effective mRNA vaccines against COVID-19.")
        st.text("")
        st.text("")
        st.markdown("***")

        
        # WORDCLOUD
        text = result.loc[result['category'] == selected_radio, 'motivation']
        new_text = [str(x) for x in text][0]
        all_stop_words = stop_words()
        wordcloud = WordCloud(stopwords=all_stop_words,  background_color="white").generate(new_text)

        #  focus of research in medicine
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.image(wordcloud.to_image(), caption='Medicine', use_column_width=True)
        st.markdown("""
                    The Nobel Prize in Physiology or Medicine is awarded for significant contributions to the field of medical science. Here are some research topics and themes that have been recognized \n
                    with the Nobel Prize in Medicine: **Genetics and Chromosomes** (e.g., 2002, 2009): Discoveries related to the structure and function of DNA, including the elucidation of the structure \n
                    of chromosomes and telomeres. The identification and study of induced pluripotent stem **cells**, which have potential applications in regenerative medicine. The design and synthesis \n
                    of molecular machines. Neuroscience and Brain Research (e.g., 2014, 2014, 2016): Contributions to the understanding of the **nervous** system etc.
                    """)

     
        
    # ECONOMICS 
    elif selected_radio == 'Economics':
        
        # award shared in economics
        filtered_economics	 = sharing_cat[sharing_cat['category'] == 'Economics'].copy()
        collab_list=["Individual", "2 laureates", "3 laureates", "4 laureates"] 
        filtered_economics['awarded_to'] = collab_list
        filtered_economics.drop(['award_shared_with'], axis=1, inplace=True)
        custom_purple_scale = ['#746969', '#249fcd', '#ff9b2f', '#fc8300', '#ffd92f']
        fig = px.pie(filtered_economics, values='count', names='awarded_to', title='Nobel Prize Jointly Awarded to Individual/Contributors for Economics',
                    color_discrete_sequence = custom_purple_scale)
        hover_template = "<b>%{label}</b><br>Value: %{value}"
        fig.update_traces(hovertemplate=hover_template)
        st.plotly_chart(fig)
        st.write("""**93 individuals have been awarded in field of economic sciences since the inception of economics science category in 1969 of which**  
                 26 indviduals have solely received the award    
                 41 individuals have shared the Nobel Prize with 1 other laureate.  
                 24 individuals have shared the Nobel Prize with 2 other laureate.  
                 2 individuals have shared the Nobel Prize with 3 other laureate.
                 """)
        st.text("")
        st.text("")
        st.markdown("***")

        # gender disparity in economics
        fig9 = px.bar(filtered_data, x="count", y="gender", color='gender', orientation='h',      
                     height=400,
                     hover_data={"category": False, 
                                 "gender": False,
                                 "count" : True},
                     hover_name="gender",
                     labels={'count': 'No.of recipients',
                             'gender': 'Gender'},
                     color_discrete_map=colours)
        st.plotly_chart(fig9)
        st.markdown("What seems unbelievable at first, only **three women** have won the Nobel Prize in Economic Sciences since the Nobel committee began awarding an economic prize in 1969, this might be attributed to the fact that recognition of research conducted in the 70s, 80s, and early 90s, a period marked by prevalent gender biases in economics and various traditional sciences. Essentially, it implies that over time, we anticipate a rise in the proportion of women Nobel laureates as societal perspectives evolve.")
        st.text("")
        st.text("")
        st.markdown("***")

        # WORDCLOUD
        text = result.loc[result['category'] == selected_radio, 'motivation']
        new_text = [str(x) for x in text][0]
        all_stop_words = stop_words()
        wordcloud = WordCloud(stopwords=all_stop_words,  background_color="white").generate(new_text)

        #  focus of research in economics
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.image(wordcloud.to_image(), caption='Economics', use_column_width=True)
        st.markdown("""Nobel Prize in Economic Sciences, is awarded for outstanding contributions to the field of economics. Here are some research topics and themes that 
                    have been recognized with the Nobel Prize in Economics are **Macroeconomic Policy** (e.g., 2011): Research on the impact of monetary and fiscal policy, 
                    as well as the dynamics of economic cycles. **Market Design** and Matching Theory (e.g., 2012, 2019): Research on the design of markets, auctions, and 
                    allocation mechanisms, including the theory of stable allocations. **Public Finance and Taxation** (e.g., 2016): Contributions to the understanding of 
                    public finance, tax policy, and the impact of government interventions on the economy.
                    """)

    
    # PEACE    
    elif selected_radio == 'Peace':   

        # award shared in peace
        filtered_peace	 = sharing_cat[sharing_cat['category'] == 'Peace'].copy()
        collab_list=["Individual", "2 laureates", "3 laureates"] 
        filtered_peace['awarded_to'] = collab_list
        filtered_peace.drop(['award_shared_with'], axis=1, inplace=True)
        custom_purple_scale = ['#746969', '#249fcd', '#ff9b2f', '#fc8300', '#ffd92f']
        fig = px.pie(filtered_peace, values='count', names='awarded_to', title='Nobel Prize Jointly Awarded to Individual/Contributors for Peace',
                    color_discrete_sequence = custom_purple_scale)
        hover_template = "<b>%{label}</b><br>Value: %{value}"
        fig.update_traces(hovertemplate=hover_template)
        st.plotly_chart(fig)
        
        st.markdown("""
                    Of the total of **111 individuals** who have won the peace prize  
                    52 indviduals have solely received the prize award  
                    52 individuals have shared the Nobel Peace Prize with 1 other laureate.  
                    7 individuals have shared the Nobel Peace Prize with 2 other laureate.
                    
                 """)
        st.text("")
        st.text("")
        st.markdown("***")

        # gender disparity in peace
        fig9 = px.bar(filtered_data, x="count", y="gender", color='gender', orientation='h',      
                     height=400,
                     hover_data={"category": False, 
                                 "gender": False,
                                 "count" : True},
                     hover_name="gender",
                     labels={'count': 'No.of recipients',
                             'gender': 'Gender'},
                     color_discrete_map=colours)
        st.plotly_chart(fig9)
        st.markdown("""
                    19 women have been honored with the Nobel Peace Prize, marking the highest number across all categories in which the Nobel Prize is being awarded.  
                    
                    Closely behind is the literature category with 17 women winning the prize. In contrast, the prize has been awarded to 92 men. 
                    """)
        st.text("")
        st.text("")
        st.markdown("***")
        
       # WORDCLOUD
        text = result.loc[result['category'] == selected_radio, 'motivation']
        new_text = [str(x) for x in text][0]
        all_stop_words = stop_words()
        wordcloud = WordCloud(stopwords=all_stop_words,  background_color="white").generate(new_text)

        #  focus in peace
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.image(wordcloud.to_image(), caption='Peace', use_column_width=True)
        st.markdown("""
                    The Nobel Peace Prize is awarded for significant contributions to promoting peace and resolving conflicts. Here are some works, efforts, and themes that have been recognized with the Nobel Peace Prize:
                        
                    **Disarmament** (e.g., 1954, 1985, 2017): Contributions to disarmament initiatives, nuclear arms control, and efforts to prevent the spread of nuclear weapons.
                    **Peaceful Revolutions and Movements** (e.g., 1983, 1989, 2011): Recognition for individuals and movements involved in nonviolent struggles for human rights, **democracy**, 
                    conflict resolution and social justice.**Women's and Children's Rights and Gender Equality** (e.g., 1976, 2011): Recognition for efforts to promote women's rights, gender equality, and the role of women in peacebuilding.
                    """)
    
    # PEACE (ORGANISATIONS)    
    elif selected_radio == 'Peace (Organisations)':
        
        
        header = dict(values=list(org_df[['Name of Organisation', 'No of Awards']].columns),
                      fill_color = '#249fcd',
                       font=dict(color='#FFFFFF'))
        cells = dict(values = [org_df['Name of Organisation'], org_df['No of Awards']],
                     align = 'center')

        st.markdown("""
                    
                        **The Nobel Peace Prize has been granted to organizations 30 times between 1901 and 2023. Out of these awards, 27 distinct organizations have been recipients and some repeat recipients like :**    

                        International Committee of the **Red Cross** that has been honoured **three times** &  
                        United Nations High Commissioner for Refugees **(UNHCR)** which has received the prize **twice**
                    """)
        fig10 = go.Figure(data=[go.Table(header=header, cells = cells)])
        fig10.update_layout(title_text='Nobel Prize Awarded Organisations',
                          width=800,
                          height=1200)
        st.plotly_chart(fig10)

       
display_content(selected_radio)

