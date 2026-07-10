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

  it('should fail to log in with missing emailId', async () => {
    const payload = {
      password: 'Qwerty123$'
    };

    const response = await request(BASE_URL)
      .post('/eaf/rest/um/user/login')
      .send(payload);

    expect(response.statusCode).toBe(400);
    expect(response.body.httpStatusCode).toBe(400);
    expect(response.body.status).toBe('Failure');
    expect(response.body.message).toBe('Please provide a valid emailId');
    expect(response.body.result.data).toBeNull();
  });

  it('should fail to log in with empty emailId', async () => {
    const payload = {
      emailId: '',
      password: 'Qwerty123$'
    };

    const response = await request(BASE_URL)
      .post('/eaf/rest/um/user/login')
      .send(payload);

    expect(response.statusCode).toBe(400);
    expect(response.body.httpStatusCode).toBe(400);
    expect(response.body.status).toBe('Failure');
    expect(response.body.message).toBe('Please provide a valid emailId');
    expect(response.body.result.data).toBeNull();
  });

  it('should fail to log in with missing password', async () => {
    const payload = {
      emailId: 'admin@eafoods.com'
    };

    const response = await request(BASE_URL)
      .post('/eaf/rest/um/user/login')
      .send(payload);

    expect(response.statusCode).toBe(400);
    expect(response.body.httpStatusCode).toBe(400);
    expect(response.body.status).toBe('Failure');
    expect(response.body.message).toBe('Please provide password');
    expect(response.body.result.data).toBeNull();
  });

  it('should fail to log in with empty password', async () => {
    const payload = {
      emailId: 'admin@eafoods.com',
      password: ''
    };

    const response = await request(BASE_URL)
      .post('/eaf/rest/um/user/login')
      .send(payload);

    expect(response.statusCode).toBe(400);
    expect(response.body.httpStatusCode).toBe(400);
    expect(response.body.status).toBe('Failure');
    expect(response.body.message).toBe('Please provide password');
    expect(response.body.result.data).toBeNull();
  });

  it('should fail to log in with a non-existent emailId', async () => {
    const payload = {
      emailId: 'nonexistent@eafoods.com',
      password: 'Qwerty123$'
    };

    const response = await request(BASE_URL)
      .post('/eaf/rest/um/user/login')
      .send(payload);

    expect(response.statusCode).toBe(404);
    expect(response.body.httpStatusCode).toBe(404);
    expect(response.body.status).toBe('Failure');
    expect(response.body.message).toBe('User not found. Please provide a valid emailId');
    expect(response.body.result.data).toBeNull();
  });

  it('should successfully log in with uppercase emailId (case insensitivity)', async () => {
    const payload = {
      emailId: 'ADMIN@EAFOODS.COM',
      password: 'Qwerty123$'
    };

    const response = await request(BASE_URL)
      .post('/eaf/rest/um/user/login')
      .send(payload);

    expect(response.statusCode).toBe(200);
    expect(response.body.httpStatusCode).toBe(200);
    expect(response.body.status).toBe('OK');
    expect(response.body.result.data.roleName).toBe('Admin');
  });

  it('should successfully log in with leading/trailing spaces in emailId', async () => {
    const payload = {
      emailId: ' admin@eafoods.com ',
      password: 'Qwerty123$'
    };

    const response = await request(BASE_URL)
      .post('/eaf/rest/um/user/login')
      .send(payload);

    expect(response.statusCode).toBe(200);
    expect(response.body.httpStatusCode).toBe(200);
    expect(response.body.status).toBe('OK');
    expect(response.body.result.data.roleName).toBe('Admin');
  });

  it('should fail to log in with an empty JSON body', async () => {
    const response = await request(BASE_URL)
      .post('/eaf/rest/um/user/login')
      .send({});

    expect(response.statusCode).toBe(400);
    expect(response.body.httpStatusCode).toBe(400);
    expect(response.body.status).toBe('Failure');
    expect(response.body.message).toBe('Please provide a valid emailId');
    expect(response.body.result.data).toBeNull();
  });

  it('should fail to log in with a malformed email format (no domain)', async () => {
    const payload = {
      emailId: 'admin',
      password: 'Qwerty123$'
    };

    const response = await request(BASE_URL)
      .post('/eaf/rest/um/user/login')
      .send(payload);

    expect(response.statusCode).toBe(404);
    expect(response.body.httpStatusCode).toBe(404);
    expect(response.body.status).toBe('Failure');
    expect(response.body.message).toBe('User not found. Please provide a valid emailId');
    expect(response.body.result.data).toBeNull();
  });

  it('should fail to log in and not be vulnerable to SQL injection in emailId', async () => {
    const payload = {
      emailId: "' OR '1'='1",
      password: 'wrongpassword'
    };

    const response = await request(BASE_URL)
      .post('/eaf/rest/um/user/login')
      .send(payload);

    expect(response.statusCode).toBe(404);
    expect(response.body.httpStatusCode).toBe(404);
    expect(response.body.status).toBe('Failure');
    expect(response.body.message).toBe('User not found. Please provide a valid emailId');
    expect(response.body.result.data).toBeNull();
  });

  it('should fail to log in and not be vulnerable to SQL injection in password', async () => {
    const payload = {
      emailId: 'admin@eafoods.com',
      password: "' OR '1'='1"
    };

    const response = await request(BASE_URL)
      .post('/eaf/rest/um/user/login')
      .send(payload);

    expect(response.statusCode).toBe(401);
    expect(response.body.httpStatusCode).toBe(401);
    expect(response.body.status).toBe('Failure');
    expect(response.body.message).toBe('Invalid Credentials');
    expect(response.body.result.data).toBeNull();
  });

  it('should return 404 when using an incorrect HTTP method (GET)', async () => {
    const response = await request(BASE_URL)
      .get('/eaf/rest/um/user/login');

    expect(response.statusCode).toBe(404);
    expect(response.body).toEqual({});
  });

  it('should fail to log in with wrong Content-Type (text/plain)', async () => {
    const response = await request(BASE_URL)
      .post('/eaf/rest/um/user/login')
      .set('Content-Type', 'text/plain')
      .send('emailId=admin@eafoods.com&password=Qwerty123$');

    expect(response.statusCode).toBe(400);
    expect(response.body.httpStatusCode).toBe(400);
    expect(response.body.status).toBe('Failure');
    expect(response.body.message).toBe('Please provide a valid emailId');
    expect(response.body.result.data).toBeNull();
  });

  it('should return 400 when sending malformed JSON syntax', async () => {
    const response = await request(BASE_URL)
      .post('/eaf/rest/um/user/login')
      .set('Content-Type', 'application/json')
      .send('{ "emailId": "admin@eafoods.com", "password": }');

    expect(response.statusCode).toBe(400);
    expect(response.body).toEqual({});
  });

});


