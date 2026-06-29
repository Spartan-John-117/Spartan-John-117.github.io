#!/usr/bin/env python3
import sqlite3
import logging

log = logging.getLogger(__name__)

def load_v_avatar(model):
    query = """
    CREATE VIEW v_avatar AS
    SELECT DISTINCT
        ACCOUNT.ACC_LOGIN,
        ACCOUNT.ACC_NAME,
        ACCOUNT.ACC_SURNAME,
        AVATAR.av_name,
        AVATAR.av_exp,
        AVATAR.av_level
    FROM 
        ACCOUNT 
    JOIN 
        AVATAR ON ACCOUNT.ACC_LOGIN = AVATAR.ACC_LOGIN
    WHERE
    AVATAR.AV_ACTIF = 1
    ORDER BY 
        ACCOUNT.ACC_LOGIN ASC, AVATAR.av_name ASC;
    """
    try:
        cur = model.con.cursor()
        cur.execute(query)
        model.con.commit()
    except sqlite3.Error as e:
        log.error(f"Erreur lors de la création de v_avatar : {str(e)}")

def load_v_ingame(model):
    query = """
    CREATE VIEW v_ingame AS
    SELECT 
        ACCOUNT.ACC_LOGIN AS acc_login,
        AVATAR.AV_NAME AS av_name,
        MOB.MOB_POS_X AS av_pos_x,
        MOB.MOB_POS_Y AS av_pos_y
    FROM 
        ACCOUNT
    JOIN 
        AVATAR ON ACCOUNT.ACC_LOGIN = AVATAR.ACC_LOGIN
    JOIN 
        PLAYINGAVATAR ON AVATAR.AV_ID = PLAYINGAVATAR.AV_ID
    JOIN 
        MOB ON PLAYINGAVATAR.MOB_ID = MOB.MOB_ID
    ORDER BY 
        ACCOUNT.ACC_LOGIN DESC, AVATAR.AV_NAME DESC;
    """
    try:
        cur = model.con.cursor()
        cur.execute(query)
        model.con.commit()
    except sqlite3.Error as e:
        log.error(f"Erreur lors de la création de v_ingame : {str(e)}")

def load_v_race_class(model):
    query = """
    CREATE VIEW v_race_class AS
    SELECT 
        RACE.RACE_KEY_NAME AS race_key_name,
        RACE.RACE_LONG_NAME AS race_long_name,
        CLASS.CLS_KEY_NAME AS cls_key_name,
        CLASS.CLS_LONG_NAME AS cls_long_name,
        (RACE.RACE_EXP_BY_LEVEL + CLASS.CLS_EXP_BY_LEVEL) AS required_exp_by_level,
        (RACE.RACE_BONUS_HP_BY_LEVEL + CLASS.CLS_BONUS_HP_BY_LEVEL) AS bonus_hp_by_level,
        (RACE.RACE_BONUS_CP_BY_LEVEL + CLASS.CLS_BONUS_CP_BY_LEVEL) AS bonus_cp_by_level
    FROM 
        RACE
    CROSS JOIN 
        CLASS
    WHERE 
        NOT EXISTS (
            SELECT 1 
            FROM RESTRICTION_CLASS_RACE 
            WHERE 
                RESTRICTION_CLASS_RACE.CLS_KEY_NAME = CLASS.CLS_KEY_NAME
                AND RESTRICTION_CLASS_RACE.RACE_KEY_NAME = RACE.RACE_KEY_NAME
        )
    ORDER BY 
        required_exp_by_level DESC, 
        bonus_hp_by_level DESC, 
        bonus_cp_by_level DESC;
    """
    try:
        cur = model.con.cursor()
        cur.execute(query)
        model.con.commit()
    except sqlite3.Error as e:
        log.error(f"Erreur : {str(e)}")

def f_account_actif(model, acc_login) -> bool:
    query = """
    SELECT COUNT(*)
    FROM AVATAR
    WHERE ACC_LOGIN = ? AND AV_ACTIF = 1;
    """
    try:
        cur = model.con.cursor()
        cur.execute(query, (acc_login,))
        result = cur.fetchone()
        return result[0] == 1
    except sqlite3.Error as e:
        log.error(f"Erreur SQL : {str(e)}")
        return False

def f_progression(model, race, cls, lvlmin, lvlmax) -> list:
    query = """
    WITH level_range AS (
        SELECT lvl
        FROM (
            SELECT ? + ROW_NUMBER() OVER () - 1 AS lvl
            FROM sqlite_master
            LIMIT (? - ? + 1)  -- Génère un nombre de lignes entre lvlmin et lvlmax
        )
        WHERE lvl BETWEEN ? AND ?
    )
    SELECT 
        level_range.lvl AS level,
        (level_range.lvl - 1) * RACE.RACE_EXP_BY_LEVEL + (level_range.lvl - 1) * CLASS.CLS_EXP_BY_LEVEL AS XP,
        CAST(RACE.RACE_HP_INIT_VALUE + (level_range.lvl - 1) * RACE.RACE_BONUS_HP_BY_LEVEL +
             CLASS.CLS_HP_INIT_VALUE + (level_range.lvl - 1) * CLASS.CLS_BONUS_HP_BY_LEVEL AS INTEGER) AS HP,
        CAST(RACE.RACE_CP_INIT_VALUE + (level_range.lvl - 1) * RACE.RACE_BONUS_CP_BY_LEVEL +
             CLASS.CLS_CP_INIT_VALUE + (level_range.lvl - 1) * CLASS.CLS_BONUS_CP_BY_LEVEL AS INTEGER) AS CP
    FROM level_range
    CROSS JOIN RACE
    CROSS JOIN CLASS
    WHERE RACE.RACE_KEY_NAME = ?
      AND CLASS.CLS_KEY_NAME = ?;
    """
    cur = model.con.cursor()
    cur.execute(query, (lvlmin, lvlmax, lvlmin, lvlmin, lvlmax, race, cls))
    return cur.fetchall()
