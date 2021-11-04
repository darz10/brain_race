import { Route, Switch, Redirect, useLocation, useHistory, Link, BrowserRouter } from "react-router-dom" 
import Auth from './components/Auth.jsx'
import MainPage from './components/MainPage.jsx'


function App() {
  return (
    <BrowserRouter>
      <Route exact path='/login'>
        <div className="login">
          <Auth/>
        </div>
      </Route>
      <Route exact path='/'>
        <div className="MainPage">
          <MainPage/>
        </div>
      </Route>
    </BrowserRouter>
  )
  }
export default App;
