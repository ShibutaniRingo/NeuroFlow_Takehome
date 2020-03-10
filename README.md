# NeuroFlow_Takehome

<p>Created by: <strong>Ziwei Jiang</strong>
<p>Language Used: <strong>Python 3</strong>
<p>Package Needed: pandas, numpy, time, datetime, matplotlib.pyplot, scipy(please install these packages before running the code below.)

<ul>
<li>DataSource
    <ul>
        <li>Csubj_measures.csv</li>
        <li>NeuroFlow Data Team Take Home Project.pdf: requirements</li>
    </ul>
</li>
<li>Code: different format for raw code.
    <ul>
        <li>NeuroFlow_Takehome_notebook.ipynb: note that part 2 SQL is also included.</li>
        <li>NeuroFlow_Takehome_notebook.html: in case you didn't have jupyter notebook installed.</li>
        <li>NeuroFlow_Takehome_Part1.py: code for part 1.</li>
    </ul>
</li>
<li>Final Deliverables: insights is also included in README.md.</li>
</ul>
<p> 
<p>_______________________________________________________________
<p>
<h4>Data Cleansing</h4>
<p>This part includes data cleansing and data preprocessing. Steps are 
<ul>
<li>Read data.
<li>Reform the "date" column.
<li>Extract subset for mood, stress, rumination, and sleep tracking.
</ul>
<h4>Data Description</h4>
<ul>
<li>The records for rumination stress and anticipatory stress is far less than records for mood and sleep.
<li>Not every user will record all the four metrics every day.
    <ul>
        <li>Some user never record their rumination stress and anticipatory stress.
        <li>Some user will record their mood and sleep for more than once in a day.
    </ul>
</ul>
<h4>Data Explorations</h4>
<p>First, we create buckets for each dataset. The criterion is rounding to the nearest integer. We would like to see the proportion of all the kind of response in each <strong>Subjective Metrics</strong> questions. After visualizing our result, we are supposed to discover that the proportion of each level for each metrics generally looks similar to each other.
<p>Next, we are going to find how will each <strong>Subjective Metrics</strong> changes for a specific user and plot these metrics' changes.
<p>Then, let's discover a little bit more about the patients. For example, for each patient, we can calculate the average score of each metrics.
<p>The relationship between average mood and sleep, rumination/anticipatory stress scores is: 
<p>mood =  1.75 +  0.18 * sleep +  0.03 * rumination stress+  0.07  * anticipatory stress
<h4>Conclusion and Improvement</h4>
<p>As we can see from the the result of one of our user (<strong>user_id=2666</strong>) , their rating for mood (<font color=#1B813E>green lines</font color=#1B813E>) and sleep quality (<font color=#DDD23B>yellow lines</font color=#DDD23B>) tend to move in the same direction, and their rating for rumination stress (<font color=#CB1B45>red lines</font color=#CB1B45>) and anticipatory stress(<font color=#113285>blue lines</font color=#113285>) seems not so related to the previous two metrics. </p>
<p><strong>What are 2-3 additional pieces of information that would be important to collect?</strong>
<ol>
<li>As mentioned above, collect all the four metrics user data within the same day, and keep tracking for more consecutive days. Thus, we can do regression on each user to explore more on the relationship between the four metrics of that specified user.
<li>If we want to see whether the therapy is making a difference, the date of each user receiving his/her therapy should be included. Thus, we can split user data by 'before therapy', 'after therapy' to prepare for an A/B testing.
<li>If possible, we can also collect data of which mental health provider does each user go to. Thus, we can do a recommendation on mental health provider choice to the patients.
</ol>
<p>Intuitively, we would say that this user's moods are affected by his/her sleeping quality, rumination stress level and anticipatory stress level. 
<ul>
    <li><strong>Sleeping quality:</strong> positively related to their mood, sometimes will affect their mood in the future.</li>
    <li><strong>Rumination stress:</strong> slightly positively related to their mood.</li>
    <li><strong>Anticipatory stress:</strong> slightly positively related to their mood.</li>
</ul>
<p>Idealy, if we can collect all the four metrics user data within the same day, and keep tracking for more consecutive days, we can do regression on mood and other metrics. 
