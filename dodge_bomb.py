import os
import sys
import pygame as pg
import random 
import time


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
bb_imgs=[]
bb_img=[]
bb_acc=[]


def get_kk_imgs(img:pg.Surface) -> dict[tuple[int, int], pg.Surface]:
    """
    引数：こうかとんのrotozoomした画像
    返り値：方向に合わせて処理された辞書型の画像
    動作：引数の画像に対して様々な方向を向いている画像を辞書型にして返り値に送る
    """
    img_flip = pg.transform.flip(img, True, False)
    kk_dict={
        ( 0, 0):pg.transform.rotozoom(img_flip,0,1.0),
        ( 0,-5):pg.transform.rotozoom(img,270,1.0),
        (+5,-5):pg.transform.rotozoom(img_flip,45,1.0),
        (+5, 0):pg.transform.rotozoom(img_flip,0,1.0),
        (+5,+5):pg.transform.rotozoom(img_flip,320,1.0),
        ( 0,+5):pg.transform.rotozoom(img,90,1.0),
        (-5,+5):pg.transform.rotozoom(img,45,1.0),
        (-5, 0):pg.transform.rotozoom(img,0,1.0),
        (-5,-5):pg.transform.rotozoom(img,315,1.0),
    }
    return kk_dict


#ボール画像と速度生成
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    引数：なし
    戻り値 ボールの画像listと速度のintlist
    画像と速度値の生成処理を行ったものをリスト化した
    """
    for r in range(1,11):
        bb_img=pg.Surface((20*r,20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    bb_accs=[a for a in range(1,11)]
    return bb_imgs,bb_accs


#画面外に対しての処理
def check_bound(rct:pg.rect)->tuple[bool,bool]:
    """
    引数：こうかとんrect or 爆弾rect
    戻り値：判定結果タプル(横座標,縦座標)
    画面内ならTrue、画面外ならFalse
    """
    yoko=True
    tate=True
    if rct.left<0 or rct.right>WIDTH:
        yoko=False
    if rct.top<0 or rct.bottom>HEIGHT:
        tate=False
    return yoko,tate


#ゲームオーバー画面の処理
def gameover(screen:pg.Surface)->None:
    """
    引数：スクリーン
    """
    #こうかとん画像ロード  
    kk_over_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk_over_rct = kk_over_img.get_rect()
    kk_over_rct.center = 300, 200

    #黒画面
    over_img=pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(over_img,(0,0,0),(0,0,WIDTH, HEIGHT))
    over_img.set_alpha(200)

    #ゲームオーバー文字
    fonto=pg.font.Font(None,80)
    text=fonto.render("GAMEOVER",True,(255,255,255))

    #各画面の描写
    screen.blit(over_img, [0, 0])
    screen.blit(text,[400,300])
    screen.blit(kk_over_img,[300,300])
    screen.blit(kk_over_img,[800,300])
    pg.display.update()
    time.sleep(5)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg") 


    #こうかとん   
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_imgs = get_kk_imgs(kk_img)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    clock = pg.time.Clock()

    #爆弾
    bb_img,bb_accs=init_bb_imgs()#爆弾の初期化
    bb_img = bb_imgs[0] 
    bb_rct=bb_img.get_rect()
    bb_rct.center=random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx=5
    vy=5
    tmr = 0
    DELTA={
        pg.K_UP:(0,-5),
        pg.K_DOWN:(0,5),
        pg.K_LEFT:(-5,0),
        pg.K_RIGHT:(5,0)
        }
    

    

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):#gameover処理
            gameover(screen)
            return
            
        speed=min(tmr//500,9)
        avx=vx*bb_accs[speed]
        avy=vy*bb_accs[speed]
        bb_img=bb_imgs[speed]
        screen.blit(bg_img, [0, 0])
        screen.blit(bb_img,bb_rct) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0]+=mv[0]
                sum_mv[1]+=mv[1]
        mv = tuple(sum_mv) 
        kk_img = kk_imgs.get(mv, kk_imgs[(0,0)])   
        kk_rct.move_ip(sum_mv)

        old_center = bb_rct.center
        bb_rct = bb_img.get_rect()
        bb_rct.center = old_center


        #ボール跳ね返り機能
        if check_bound(kk_rct)!=(True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])#移動を０にする
        bb_rct.move_ip(avx,avy)
        screen.blit(kk_img, kk_rct)
        yoko,tate=check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
