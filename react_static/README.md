# React components.


## How to use:
### Dependencies

Connect react and babel.
```html
<script src="https://unpkg.com/babel-standalone@6/babel.min.js"></script>
<script crossorigin src="https://unpkg.com/react@17/umd/react.development.js"></script>
<script crossorigin src="https://unpkg.com/react-dom@17/umd/react-dom.development.js"></script>
```

Connect all components.
````html
<script src="/<your_static_folder>/react_components/pages/HomePage.js"></script>
<script src="/<your_static_folder>/react_components/pages/AuthPage.js"></script>
...
````

Styling dependencies:
````html
<script src="https://cdn.tailwindcss.com"></script>
````

### Initialize on HTML page. 
````html
<body>
    <div id="home-page"></div>
</body>

<script>
    let container = document.getElementById("home-page");
    ReactDOM.render(React.createElement(HomePage, {
        exampleProps1: "exampleProps1",
        exampleProps2: "exampleProps2"
    }), container);
</script>
````
### 