const request = require('supertest');

const BASE_URL = 'https://dev.eafoods.com';

describe('EA Foods Login API Tests', () => {

  it('should successfully log in with valid credentials', async () => {
    const loginPayload = {
      emailId: 'admin@eafoods.com',
      password: 'Qwerty123$'
    };

    const response = await request(BASE_URL)
      .post('/eaf/rest/um/user/login')
      .send(loginPayload);

    console.log('Valid Login Status:', response.statusCode);
    console.log('Valid Login Headers:', response.headers);
    console.log('Valid Login Response Body:', response.body);

    expect(response.statusCode).toBe(200);

    expect(response.headers['authorization']).toBeDefined();
    expect(response.headers['authorization']).toContain('Bearer');

    expect(response.headers['refreshtoken']).toBeDefined();
    expect(response.headers['refreshtoken']).toContain('Bearer');

    expect(response.body.httpStatusCode).toBe(200);
    expect(response.body.status).toBe('OK');
    expect(response.body.message).toBe('Successfully logged In');
    
    expect(response.body.result.data.roleName).toBe('Admin');
  });

  it('should fail to log in with invalid credentials', async () => {
    const invalidPayload = {
      emailId: 'admin@eafoods.com',
      password: 'wrongpassword'
    };

    const response = await request(BASE_URL)
      .post('/eaf/rest/um/user/login')
      .send(invalidPayload);

    console.log('Invalid Login Status:', response.statusCode);
    console.log('Invalid Login Response Body:', response.body);

    expect(response.statusCode).toBe(401);

    expect(response.body.httpStatusCode).toBe(401);
    expect(response.body.status).toBe('Failure');
    expect(response.body.message).toBe('Invalid Credentials');
    expect(response.body.result.data).toBeNull();
  });

});
