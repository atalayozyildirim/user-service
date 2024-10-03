from db.db import dynamodb
from db.Model.UserModel import UserModel

table= dynamodb.Table('users')

async def get_user_username(username: str):
    try:
        if username is None:
            return {"message": "Username is required"}

        if type(username) != str:
            return {"message": "Username should be a string"}

        user = table.get_item(
            Key={
                'username': username
            }
        )
        if 'Item' in user:
            return user['Item']
        else:
            return {"message": "User not found"}
    except Exception as e:
        return {"message": "Server error", "error": str(e)}


async def get_user():
    return {"message": "me"}

async def get_user_by_id(userid: int):
    try:
        if userid is None:
            return {"message": "User id is required"}
        if type(userid) != int:
            return {"message": "User id should be an integer"}
        user = table.get_item(
            Key={
                'userid': userid
            }
        )
        if 'Item' in user:
            return user['Item']
        else:
            return {"message": "User not found"}
    except Exception as e:
        return {"message": "Server error", "error": str(e)}

async def add_user_controller(user: UserModel):
    try:
        if user is None:
            return {"message": "User data is required"}

        existsUser =  table.get_item(
            Key={
                'username': user.username
            }
        )
        if 'Item' in existsUser:
            return {"message": "User already exists"}

        print(existsUser)
        user_dict = user.dict()
        table.put_item(Item=user_dict)

        return {"message": "User added successfully", "data": user_dict}

    except Exception as e:
        return {"message": "Server error", "error": str(e)}


async def update_user_controller(user_data: dict):
    try:
        if user_data is None:
            return {"message": "UserData is required"}

        if 'username' not in user_data:
            return {"message": "Username is required in userData"}

        user = table.get_item(
            Key={
                'username': user_data['username']
            }
        )
        if 'Item' not in user:
            return {"message": "User not found"}

        update_expression = 'SET'
        expression_attribute_values = {}

        for key, value in user_data.items():
            if key != 'username':
                update_expression += f' {key} = :{key},'
                expression_attribute_values[f':{key}'] = value

        update_expression = update_expression[:-1]
        table.update_item(
            Key={
                'username': user_data['username']
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return {"message": "User updated successfully"}
    except Exception as e:
        return {"message": "Server error", "error": str(e)}

async def delete_user_controller(username: str):
    try:
        if username is None:
            return {"message": "Username is required"}

        existin_user =  table.get_item(
            Key={
                'username': username
            }
        )

        if 'Item' not in existin_user:
            return {"message": "User not found"}

        table.delete_item(
            Key={
                'username': username
            }
        )
        return {"message": "User deleted successfully"}
    except Exception as e:
        return {"message": "Server error", "error": str(e)}