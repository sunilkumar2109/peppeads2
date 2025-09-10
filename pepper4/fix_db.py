from app import app, db, User

with app.app_context():
    try:
        # Check if 'is_admin' column exists
        # This requires introspecting the table, which can be tricky directly with SQLAlchemy in all DBs.
        # A simpler way for SQLite is to try adding it and catch the error if it exists.
        # Or, just check pragma table_info for SQLite
        cursor = db.session.connection().connection.cursor()
        cursor.execute("PRAGMA table_info(user);")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'is_admin' not in columns:
            print("Column 'is_admin' does not exist. Adding it...")
            db.session.execute(db.text('ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0'))
            db.session.commit()
            print("Column 'is_admin' added successfully.")
        else:
            print("Column 'is_admin' already exists. Skipping column addition.")

        # Set all users to is_admin=False first, then specific admin to True
        print("Ensuring all users have is_admin set to False...")
        # Update all users to False, then selectively update admin
        # Using update() for efficiency
        db.session.query(User).update({User.is_admin: False})
        db.session.commit()
        print("All existing users set to is_admin=False.")

        # Create or update the 'admin' user
        admin_user = User.query.filter_by(email='admin').first()
        if not admin_user:
            print("Creating default admin user: admin/admin...")
            admin_user = User(email='admin', is_admin=True)
            admin_user.set_password('admin')
            db.session.add(admin_user)
            db.session.commit()
            print("Default admin user created and set to admin.")
        elif not admin_user.is_admin:
            print("Existing 'admin' user found but not admin. Setting to admin...")
            admin_user.is_admin = True
            db.session.commit()
            print("Existing 'admin' user set to admin.")
        else:
            print("Admin user already exists and is an admin.")

        print("Database update script completed successfully.")

    except Exception as e:
        print(f"An error occurred during database update: {e}")
        db.session.rollback() 