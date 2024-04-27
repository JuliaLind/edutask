const backend_url = Cypress.env('BACKEND_URL')



describe('Todo', () => {
    // define variables that we need on multiple occasions
    let uid // user id
    let email // email of the user

    beforeEach(function () {
        // create a fabricated user from a fixture
        cy.fixture('user.json')
        .then((user) => {
            cy.request({
                method: 'POST',
                url: `${backend_url}/users/create`,
                form: true,
                body: user
            })
            .then((response) => {
                uid = response.body._id.$oid
                email = user.email

                cy.request({
                    method: 'POST',
                    url: `${backend_url}/tasks/create`,
                    form: true,
                    body: {
                    'title': "My first task",
                    'description': "Test description",
                    'userid': uid,
                    'url': 'testurl',
                    'todos': "My first todo" // inte helt säker på varför det måste vara string här, men det verkar funka (kollat mot databas) och array funkar inte
                    }
                })
                .then((response) => {
                    cy.log('my resonsebody', response.body)
                    cy.visit('/')
                    // login
                    cy.contains('div', 'Email Address')
                        .find('input[type=text]')
                        .type(email)
                    cy.get('form')
                    .submit()
                    // click on task for detailed view
                    cy.get('.container')
                    .contains('.title-overlay', 'My first task')
                    .parents('a')
                    .click()
                })
            })
        })
    })


    it('This test is only to make sure that the intial conditions are set as expected', () => {
        cy.get('.todo-list')
        .find('.todo-item').last()
        .find('.editable')
        .should('have.text', 'My first todo')
    })

    it('R8UC1 - Add button should be disabled if description is not entered', () => {
        cy.get('.todo-list')
        .find('.inline-form')
        .find('input[type=text]')
        .clear() // clear the input field to ensure that it's empty
        .get('.inline-form input[value="Add"]')
        .should('be.disabled')
    })

    it('R8UC1 - Add button should not be disabled if description is entered', () => {
        cy.get('.todo-list')
        .find('.inline-form')
        .find('input[type=text]')
        .type("This is my second task")
        .get('.inline-form input[value="Add"]')
        .should('not.be.disabled')
    })

    it('R8UC1 - When a task has been added it should appear last on the list', () => {
        const secondTodoDescr = "This is my second todo"

        cy.get('.todo-list')
        .find('.inline-form')
        .find('input[type=text]')
        .type(secondTodoDescr)
        .get('.inline-form input[value="Add"]')
        .click()
        .get('.todo-list')
        .find('.todo-item').last()
        .find('.editable')
        .should('have.text', secondTodoDescr)
    })

    it('R8UC2 - Toggle todo item Active->Done->Active', () => {
        cy.contains('.todo-item', 'My first todo')
            .find('.checker')
            .should('not.have.class', 'checked')
            .and('have.class', 'unchecked') // assert that todo is initially active
            .click() // click the icon
            .should('not.have.class', 'unchecked')
            .and('have.class', 'checked') // assert that todo is done after the click
            .parents('.todo-item')
            .find('.editable')
            .should('have.css', 'text-decoration-line', 'line-through') // assert that the done todo is strike through
            .parents('.todo-item')
            .find('.checker', '.checked')
            .click() // click the icon again
            // .wait(5000) // uncomment the wait time if the test is not passing, sometimes it takes longer time
            .should('not.have.class', 'checked')
            .and('have.class', 'unchecked') // assert that todo is now active again
            .parents('.todo-item')
            .find('.editable')
            .should('not.have.css', 'text-decoration-line', 'line-through') // assert that todo is no longer strike-through
    })

    it('R8UC3 - When the x symbol behind a task is clicked the task should be removed from the list', () => {
        cy.intercept('DELETE', `**/todos/byid/*`).as('deleteTodo')

        const firstTodoDescr = "My first todo"
        cy.contains('.todo-item .editable', firstTodoDescr)
        .parents('.todo-item')
        .find('.remover')
        .click()

        cy.wait('@deleteTodo').then((interception) => {
            // first one is not technically an assert, 
            // but to make sure that the request to
            // backend has resulted in a response
            // before asserting if the item has been 
            // removed from the view
            assert.equal(interception.response.statusCode, 200)

            cy.wait(20000).contains('.todo-item .editable', firstTodoDescr).should('not.exist')
        })
    })

    afterEach(function () {
        // clean up by deleting the user 
        // and associated tasks and todos from the database
        cy.request({
            method: 'DELETE',
            url: `${backend_url}/users/${uid}`
        })
    })
})