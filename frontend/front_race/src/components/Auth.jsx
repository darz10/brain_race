// import './style.css';
import { Row, Form, Input, Button, Checkbox } from 'antd';
// import "../index.css"


const onFinish = (values) => {
  fetch(`http://127.0.0.1:8000/v1/login`, {
    headers: {
      'Content-Type': 'multipart/form-data;',
      'Access-Control-Allow-Origin': '*',
      'Accept-Encoding': 'gzip, deflate, br',
      'Connection': 'keep-alive',

    },
    credentials: 'same-origin',
    method: 'POST',
    body: JSON.stringify({'username': values.username, '  password': values.password})
  }).then(response => {});
};

const onFinishFailed = (errorInfo) => {
  console.log('Failed:', errorInfo);
};

const Auth = (props) => {
return(
    <div class="block_login">
      <Row justify="center" type="flex" align="middle" style={{marginTop: "20%"}}>
        <Form
          name="login_form"
          labelCol={{
            span: 8,
          }}
          wrapperCol={{
            span: 16,
          }}
          initialValues={{
            remember: true,
          }}
          onFinish={onFinish}
          onFinishFailed={onFinishFailed}
          autoComplete="off"
          style={{marginLeft: "10%"}, {marginRight: "10%"}, {minHeight: "calc(100vh - 950px)"}}
        >
          <Form.Item
            label="Username"
            name="username"
            rules={[
              {
                required: true,
                message: 'Please input your username!',
              },
            ]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Password"
            name="password"
            rules={[
              {
                required: true,
                message: 'Please input your password!',
              },
            ]}
          >
            <Input.Password />
          </Form.Item>
          
          <Form.Item
            name="remember"
            valuePropName="checked"
            wrapperCol={{
              offset: 8,
              span: 16,
            }}
          >
            <Checkbox>Remember me</Checkbox>
          </Form.Item>

          <Form.Item
            wrapperCol={{
              offset: 8,
              span: 16,
            }}
          >
            <Button type="primary" htmlType="submit">
              Submit
            </Button>
          </Form.Item>
        </Form>
      </Row>
    </div>
)
}

export default Auth