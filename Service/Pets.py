from Model.Pets import Pets
from flask import jsonify
from PBD_config import db_init as db

class Pet_operation():
    def __init__(self):
        super().__init__()

    def register_pet(self, Pname, Powner, Pimage, Pgender, Pvariety, Pbirth):
        new_pet = Pets(
            Pname=Pname,
            Powner=Powner,
            Pimage=Pimage,
            Pgender=Pgender,
            Pvariety=Pvariety,
            Pbirth=Pbirth
        )
        db.session.add(new_pet)
        db.session.commit()

        return jsonify({'code': 0, 'message': '宠物注册成功！', 'data': new_pet.to_dict()})

    def get_pet_info(self, Pno):
        pet = Pets.query.filter_by(Pno=Pno).first()
        if not pet:
            return None
        return pet.to_dict()

    def update_pet(self, Pno, Pname, Pimage, Pgender, Pvariety, Pbirth):
        pet = Pets.query.filter_by(Pno=Pno).first()
        if not pet:
            return jsonify({'code': -1, 'message': '宠物不存在！', 'data': {}})
        pet.Pname = Pname
        if Pimage:
            pet.Pimage = Pimage
        pet.Pgender = Pgender
        pet.Pvariety = Pvariety
        pet.Pbirth = Pbirth
        db.session.commit()

        return jsonify({'code': 0, 'message': '宠物信息更新成功！', 'data': pet.to_dict()})

    def delete_pet(self, Pno):
        pet = Pets.query.filter_by(Pno=Pno).first()
        if not pet:
            return jsonify({'code': -1, 'message': '宠物不存在！', 'data': {}})
        db.session.delete(pet)
        db.session.commit()
        return jsonify({'code': 0, 'message': '宠物删除成功！', 'data': {}})