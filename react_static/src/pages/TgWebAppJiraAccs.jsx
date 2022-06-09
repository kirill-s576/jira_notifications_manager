function TgWebAppJiraAccs({loginPath}){

    const [user, setUser] = React.useState({
        id: null,
        first_name: null,
        last_name: null,
        username: null,
        language_code: null
    })
    const [verifiedInitData, setVerifiedInitData] = React.useState(null)
    const [jiraAccounts, setJiraAccounts] = React.useState([])
    const [errorMessage, setErrorMessage] = React.useState(null)
    const [mainButtonClicked, setMainButtonClicked] = React.useState(false)


    const verifyInitData = (unverifiedInitData) => {
        let queryParams = new URLSearchParams({
            init_data: unverifiedInitData
        })
        fetch("/web_app/verify_init_data?" + queryParams, {
            method: "GET",
        })
          .then(response => response.json())
          .then((data) => {
              setVerifiedInitData(unverifiedInitData)
              setUser(data)
          })
          .catch(error => {
              setVerifiedInitData("UNVERIFIED")
              setErrorMessage(`Verification Error: ${error}`)
          });
    }

    const fetchJiraAccounts = (initData) => {
        let headers = {
            "init-data": initData
        }
        fetch('/web_app/jira_accounts', {
            method: "GET",
            headers: headers
        })
            .then(response => response.json())
            .then((data) => {
                setJiraAccounts(data)
            })
            .catch(error => {
                setErrorMessage(`Fetch Jira Accounts Error: ${error}`)
            });
    }

    const addNewAccountTrigger = () => {
        if (!verifiedInitData) {
            return
        }
        let headers = {
            "init-data": verifiedInitData
        }
        fetch('/web_app/jira_accounts', {
            method: "POST",
            headers: headers
        })
            .then(response => response.json())
            .then((data) => {
                console.log(data)
            })
            .catch(error => {
                setErrorMessage(`Headers: ${error}`)
            });
    }

    React.useEffect(() => {
        // On page ready
        Telegram.WebApp.ready()
        verifyInitData(Telegram.WebApp.initData)
        Telegram.WebApp.MainButton.enable()
        Telegram.WebApp.MainButton.setText("Add Account")
        Telegram.WebApp.MainButton.show()
    }, [])

    React.useEffect(() => {
        if (verifiedInitData && verifiedInitData !== "UNVERIFIED"){
            fetchJiraAccounts(verifiedInitData)
            Telegram.WebApp.MainButton.onClick(mainButtonClick)
        }
    }, [verifiedInitData])

    const getErrorMessageJSX = () => {
        return (
            <div style={{ color: "var(--tg-theme-text-color)" }}>
                {errorMessage}
            </div>
        )
    }

    const mainButtonClick = () => {
        if (!mainButtonClicked) {
            addNewAccountTrigger()
        }
        Telegram.WebApp.close()
    }

    const getJiraAccountsJSX = () => {
        return (
            <div className="w-full flex flex-wrap flex-row">
                <h3 style={{color: "var(--tg-theme-text-color)"}}>Your accounts:</h3>
                {
                    jiraAccounts.concat(jiraAccounts, jiraAccounts, jiraAccounts).map((jiraAccount) => (
                        <div key={jiraAccount.id} className="container w-80 mx-auto">
                            <div
                                className="my-5 w-full items-center justify-center overflow-hidden rounded-2xl bg-slate-200 shadow-xl"
                            >
                                <div className="h-24 bg-white"></div>
                                <div className="-mt-20 ml-10 flex justify-start">
                                    <img className="h-32 rounded-full"
                                         src={jiraAccount.avatar_url}/>
                                </div>
                                <div className="flex mr-10 justify-end text-black">
                                    <p>{jiraAccount.resource_name}</p>
                                </div>
                                <div className="mt-5 mb-1 px-3 text-center text-lg">
                                    {jiraAccount.resource_name}
                                </div>
                            </div>
                        </div>
                    ))
                }
            </div>
        )
    }

    const getEmptyJiraAccountsJsx = () => {
        return (
            <div style={{ color: "var(--tg-theme-text-color)" }}>
                <h3>No one account connected...</h3>
            </div>
        )
    }

    return (
        <div style={{ minHeight:"var(--tg-viewport-height)"}}>
            {getErrorMessageJSX()}
            {jiraAccounts.length > 0 ? getJiraAccountsJSX() : getEmptyJiraAccountsJsx()}
        </div>
    )
}