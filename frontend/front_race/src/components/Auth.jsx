// import './style.css';
// import "../index.css"


const handleSubmit = (values) => {
  console.log(values);
  fetch(`http://127.0.0.1:8000/v1/login`, {
    headers: {
      'Content-Type': 'application/json;',
      'Access-Control-Allow-Origin': '*',
      'Accept-Encoding': 'gzip, deflate, br',
      'Connection': 'keep-alive',

    },
    credentials: 'same-origin',
    method: 'POST',
    body: JSON.stringify({'username': values.username, 'password': values.password})
  }).then(response => {});
};

const onFinishFailed = (errorInfo) => {
  console.log('Failed:', errorInfo);
};

const Auth = (props) => {
return(
    <div>
      <div class="changer_form">
        <button class="login">Login</button>
        <button class="register">Register</button>
      </div>
      <div class="block_login">
        <form class="form_auth" onSubmit={handleSubmit}>
          <label>
            <input type="text" class="username" placeholder="Username" required/>
          </label>
          <label>
            <input type="password" class="password" placeholder="Password" required/>
          </label>
          <input type="submit" class="button_auth" value="Log in" />
        </form>
      </div>
    </div>
)
}

export default Auth