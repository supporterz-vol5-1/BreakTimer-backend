[![pytest](https://github.com/supporterz-vol5-1/BreakTimer-backend/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/supporterz-vol5-1/BreakTimer-backend/actions/workflows/test.yml)
[![Deploy to heroku](https://github.com/supporterz-vol5-1/BreakTimer-backend/actions/workflows/heroku.yml/badge.svg?branch=main)](https://github.com/supporterz-vol5-1/BreakTimer-backend/actions/workflows/heroku.yml)

# BreakTimer-backend

This repogitory is a backend for *BreakTimer*.


## API endpoints

- `/api/register/<username>`, `GET`
    Register user. If `username` exists already, return `412` as status code.
    Return token. The token is show only once. **Dont forget memorize it**.

    <!-- ```plantuml                                -->
    <!-- Editor->API : GET /api/register/<username> -->
    <!-- API->DB : The user exists already?         -->
    <!-- DB->API : Information                      -->
    <!-- alt Exists already                         -->
    <!--    API->Editor : Return 412                -->
    <!-- else Not Exist                             -->
    <!--     API->DB : Register user                -->
    <!--     API->Editor : Return token             -->
    <!-- end                                        -->
    <!-- ```                                        -->

- `/api/<username>`, `POST`
    **REGACY ENDPONINT**
    Register work time.
    The request must has json like below.
    ```json
    {
        "body": {
            "token": <TOKEN>,
            "work_time": <float(seconds):work_time>,
            "filetype": <FILETYPE>
        }
    }
    ```

- `/api/<username>`, `GET`
    Return specified user's work times at last 7 days.
    If the user does not exist, return 404.
    Response has json like below.
    ```json
    [
        {"python": 100, "ruby": 3000},
        {"python": 100, "ruby": 3000},
        {"python": 100, "ruby": 3000},
        {"python": 100, "ruby": 3000},
        {"python": 100, "ruby": 3000},
        {"python": 100, "ruby": 3000},
        {"python": 100, "ruby": 3000},
    ]

    ```

- `/api/<username>/<filetype>`, `GET`
    Return specified user's specified language work time at last 7 days.
    If the user does not exist, return 404.
    Response has json like below.
    ```json
    [
        {"python": 0},
        {"python": 100},
        {"python": 1200},
        {"python": 100},
        {"python": 100},
        {"python": 100},
        {"python": 100},
    ]
    ```

- `/api/start/<username>`, `POST`
    Register specified user's work time.
    If the use have started work already, old work register as finished one.
    The request must has json like below.
    ```json
    {
        "body": {
            "token": <TOKEN>,
            "filetype": <FILETYPE>
        }
    }
    ```

    <!-- ```plantuml                              -->
    <!-- Editor->API : POST:/api/start/<username> -->

    <!-- API->DB : Start already?                 -->

    <!-- DB->API : Information                    -->

    <!-- opt Exists already                       -->
    <!--     API->API : Calculate work time       -->
    <!--     API->DB : Stop and register old work -->
    <!-- end                                      -->

    <!-- API->DB : Register work as start one     -->
    <!-- ```                                      -->

- `/api/stop/<username>`, `POST`
    Register specified user's work as finished one.
    If the work does not exist, nothing happen.
    The request must has json like below.
    ```json
    {
        "body": {
            "token": <TOKEN>,
            "filetype": <FILETYPE>
        }
    }
    ```

    <!-- ```plantuml                                             -->
    <!-- Editor->API : POST:/api/stop/<username>                 -->

    <!-- API->DB : Exists corresponding one?                     -->

    <!-- DB->API : Information                                   -->

    <!-- opt Exists                                              -->
    <!--     API->API : Calculate work time if exists            -->
    <!--     API->DB : Stop work and register it as finifhed one -->
    <!-- end                                                     -->
    <!-- ```                                                     -->
