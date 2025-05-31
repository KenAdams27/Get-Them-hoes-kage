     for obstacle in obstacle_rect_list:
                if selected_player_left is True:
                    if obstacle.collidepoint(player_left_rect.centerx,player_left_rect.centery):
                        game_active=False
                if selected_player_right is True:
                    if obstacle.collidepoint(player_right_rect.centerx,player_right_rect.centery):
                        game_active=False