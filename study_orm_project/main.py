from study_orm_project.crud import *

# ✅ 1. Создаём пользователя
user = create_user("Alice")
print(f"Создан пользователь: id={user.id}, name={user.name}")

# ✅ 2. Создаём подписку
subscription_id = create_subscription("Netflix")
print(f"Создана подписка с id={subscription_id}")

# ✅ 3. Привязываем пользователя к подписке
subscribe_user(user_id=user.id, subscription_id=subscription_id, start_date=date.today())
print(f"Пользователь {user.name} подписан на подписку с id={subscription_id}")

# ✅ 4. Получаем подписки пользователя
subs = get_user_subscriptions(user.id)
print("Подписки пользователя:")
for sub in subs:
    print(f"- {sub.name}")

# ✅ 5. Отписываем пользователя от подписки
unsubscribe_user(user.id, subscription_id)
print(f"Пользователь {user.name} отписан от подписки с id={subscription_id}")

# ✅ 6. Проверка подписок после удаления
subs = get_user_subscriptions(user.id)
print("Подписки после отписки:")
if subs:
    for sub in subs:
        print(f"- {sub.name}")
else:
    print("Нет активных подписок")

# ✅ 7. Удаляем пользователя
delete_user(user.id)
print(f"Пользователь {user.name} удалён")