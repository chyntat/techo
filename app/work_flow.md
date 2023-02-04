## workflow for the landing page 
- a single page application 
  - left, right and middle panels. 
  - left panel to contain a calendar in the bottom
  - left panel will have keywords, topics, sentiment etc tagged.
  - middle panel will have the posts
    - top will have the post from day before yesterday
    - middle will have the post from yesterday
    - bottom will have the post from today (editable)
  - middle panel bottom to have a button
    - on click of the button, the post will be sent to the backend
  - right panel will be empty for now


## APIs
- `get_previous_posts`
    - response:
      - ```python
        {
          'day_before_yesterday': {
              'post': 'post text',
              'keywords': ['keyword1', 'keyword2'],
              'topics': ['topic1', 'topic2'],
              'sentiment': 'positive',
              },  
          },
          'yesterday': {
                'post': 'post text',
                'keywords': ['keyword1', 'keyword2'],
                'topics': ['topic1', 'topic2'],
                'sentiment': 'positive',
                },  
          },
          'today': { # if today's post is not found, we will send empty values for all keys. 
                'post': 'post text',
                'keywords': ['keyword1', 'keyword2'],
                'topics': ['topic1', 'topic2'],
                'sentiment': 'positive',
                },  
        }
      ```
- `search_posts`
    - request:
      - ```python
        {
          'emotion_tag': "a day with extreme happiness",
        }
      ```
    - response:
      - ```python
        {
          'posts': [ # the posts will be sorted by date in descending order (recent first)
            {
              'post': 'post text',
              'keywords': ['keyword1', 'keyword2'],
              'topics': ['topic1', 'topic2'],
              'sentiment': 'positive',
              'date_posted': '2019-01-01',
            },
            {
              'post': 'post text',
              'keywords': ['keyword1', 'keyword2'],
              'topics': ['topic1', 'topic2'],
              'sentiment': 'positive',
                'date_posted': '2019-01-01',
            },
          {
              'post': 'post text',
              'keywords': ['keyword1', 'keyword2'],
              'topics': ['topic1', 'topic2'],
              'sentiment': 'positive',
                'date_posted': '2019-01-01',
            },
          ]
        }
      ```
      



#### Bugs to fix
- check if user exists while posting a blog