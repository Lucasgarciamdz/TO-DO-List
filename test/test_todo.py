import os
import sys
import unittest
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.main import app, db


class TestTodoApp(unittest.TestCase):
    def setUp(self):
        # Set up a test database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up the test database
        db.session.remove()
        db.drop_all()

    def test_home_page(self):
        with app.app_context():
            response = self.app.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'To Do App', response.data)


if __name__ == '__main__':
    unittest.main()
