# IDA: UI Testing for everyone


Thank you for your visit.
- Ida was built for performing repetitive UI tests and can be highly scalable.
- Give her a try no matter if you're end-user or a team of developers.
- No prior developer knowledge required.
- For any questions write me to uros.dolzan@gmail.com
- If you find Ida please consider buying me a coffee: https://www.buymeacoffee.com/qtxtz7q5f5M


# Prerequisites

Currently, only Google Chrome is supported.
You'll need to learn how to find elements. You can do it in no time,
check the links:
- https://www.wikihow.com/Inspect-Element-on-Chrome
- https://www.toolsqa.com/selenium-webdriver/inspect-element-in-chrome/

_(search for: Inspect the elements using the DOM panel of DevTools)_

You will see that every element can have various attributes. For testing with Ida
search for: id, class and name. You will want unique identifier to make sure
Ida will operate with desired element.

# Project setup

Unzip mac or win version of zip and unzip it.
Go to \dist\library

### Settings

Go to \dist\library\settings\, open **settings.json** and enter url:

	"url": "https://www.nb3.si"


Furthermore, you can add your own custom constants, i.e. username, password or whatever you need.
You can call constants in sequences with keyword **#constant:** before name of the constant.

	"constants": [
		{
			"name": "username",
			"value": "myUsername"
		},
		{
			"name": "password",
			"value": "myPassword"
		}
	]




### Sequences

Go to \dist\library\sequences\ where you can create and add multiple **.json files**.
You can split testing scenarios over multiple .json files and
control execution order with naming files accordingly (there are no rules), i.e.:

- 00100_login.json
- 00200_modify_customer_address.json
- 00300_create_new_order.json

Inside every json file you can have as many sequences as you need. I recommend splitting sequences between multiple files based on common action. You only have to be careful to maintain
valid json format of the file (you can always validate it online).

First Ida will open website from settings and begin running test sequences.
Following 00100_login.json example you create sequence for each action, i.e.:

`{
	"desc": "Login: username",
	"type": "input",
	"search": [
		"name",
		"Username"
	],
	"insertText": "myUsername"
}`


Or, using constant username you can create sequence like this:

`{
	"desc": "Login: username",
	"type": "input",
	"search": [
		"name",
		"Username"
	],
	"insertText": "#constant:password"
}`


Each sequence file must contain only 1 array of sequences and are added 
in the order of execution in the "seq" key. If your website requires login,
you need to go to login page, enter username, password and press login button.
In sequences, you would have to insert following json inside "seq" key.

`{
  "seq":
  ~~insert_array_of_sequences_like_example_below~~
}`



    [{
      "desc": "Login: username",
      "type": "input",
      "search": [
        "name",
        "Username"
      ],
      "insertText": "myUsername"
    },
    {
      "desc": "Login: password",
      "type": "input",
      "search": [
        "name",
        "Password"
      ],
      "insertText": "myPassword"
    },
    {
      "desc": "Login button pressed",
      "type": "click",
      "search": [
        "xpath",
        "//*[contains(text(), 'LOGIN')]"
      ],
      "wait": 1
    }]






**Structure of sequence json file:**

**"desc"** - sequence description for logging (+)

**"type"** - type of interaction (+):
            - "click" (click on a button, menu, etc.)
            - "input" (insert text or choosing dropdown)
            - "function" (execute Javascript function)  (++)

**"search"** - Array of 2 elements `["x", "b"]` (+)
            x - unique attribute you want to identify the element by. That can be:
                "id", "name", "class", xpath, css_selector
            y - value of the above attribute

**"insertText"** - when using type: "input", Ida will insert entered text to found input text field

**"wait"** - if you want Ida to wait after this sequence, enter number of seconds

**"skip"** - set it to true if you would like Ida to skip it

**"common_id"** - enter common id when using common in the sequence

###### (+) mandatory; (++) future release


### Introducing commons
Go to \dist\library\commons\ where you can create and add multiple **.json files**.
You can create and add multiple **.json files** to the **commons** sub folder.
Commons are design to avoid entering repetitive sequences.
Commons can be used only as clicks.

_Example of Common_

    {
      "skip": false,
      "id": "confirmButton",
      "desc": "",
      "type": "click",
      "search": [
        "xpath",
        "//*[contains(@id, 'btnConfirm')]"
      ],
      "wait": 0
    }


_Use of Common in Sequences:_

    {
      "desc": "Save new customer",
      "common_id": "confirmButton"
    }

### Example
Please check example folder for reference. You can even invert
folders: 
- rename folder example to library
- rename folder library to example