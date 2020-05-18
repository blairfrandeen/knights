from mazes import MazeLocation, Maze
from generic_search import bfs, dfs, astar, node_to_path
from typing import Tuple, List
from maze_graphics import MazeWin


def attack(start: Tuple, dest: Tuple, obstacles: List[Tuple]):
    m_start = MazeLocation(row=start[0], column=start[1])
    m_goal = MazeLocation(row=dest[0], column=dest[1])
    m_obs = []
    for o in obstacles:
        m_obs.append(MazeLocation(row=o[0], column=o[1]))

    m = Maze(start=m_start, goal=m_goal, obstacles=m_obs)
    distance = m.euclidian_distance()
    solution = astar(m.start, m.goal_test, m.successors, distance)
    if solution:
        path = node_to_path(solution)
        return len(path) - 1

    return None


def data_builder(data_string: str):
    m = Maze(data_string)
    obstacle_list = []
    for o in m.obstacles:
        obs = (o.row, o.column)
        obstacle_list.append(obs)
    return [(m.start.row, m.start.column),
            (m.goal.row, m.goal.column),
            obstacle_list]

if __name__ == '__main__':
    # display(s_test, g_test, o_test)

    data_test = ('''\
    *************************
    *   *                   *
    *   *                   *
    * S *   *****************
    *   *   *     * *       *
    *********     * *       *
    *       *     *E*       *
    *       *     * *       *
    *************************''')  # 8 moves

    unreachable = ('''\
    ***************************************************************
    ***************************************************************
    **  S                                                        **
    **                                                     E     **
    ***************************************************************
    ***************************************************************''')  # should return None

    failure =('''\
    S                   
                        
                        
                        
                        
          * *           
         *   *          
           E            
         *   *          
          * *           
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        ''')

    failure2 = ('''\
                                                                          
                                                                          
                                                                          
                                                                          
                                 *******                                  
                               ***********                                
                             ***************                              
                            ****         ****                             
                           ****           ****                            
                           ***             ***                            
                          ***               ***                           
                          **                 **                           
                         **                  ***                          
                                             ***                          
                                             ***                          
                                           S ***                E         
                                             ***                          
                                             ***                          
                         **                  ***                          
                          **                 **                           
                          ***               ***                           
                           ***             ***                            
                           ****           ****                            
                            ****         ****                             
                             ***************                              
                               ***********                                
                                 *******                                  
                                                                          
                                                                          
                                                        ''')

    arrow1 = ('''\
                                                                          
                                                                      
                                       *                              
                                      ***                             
                                      ****                            
                                      *****                           
                                       *****                          
                                        *****                         
                                         *****                        
                                          *****                       
                                           *****                      
                                            *****                     
                                             *****                    
                                              ******                  
                                               ******                 
     S                                          *****       E         
                                                ****                  
                                               ****                   
                                              ****                    
                                             ****                     
                                            ****                      
                                           ****                       
                                          ****                        
                                         ****                         
                                        ****                          
                                       ****                           
                                       ***                            
                                        *                             
                                                                      
                                                                     ''')

    f = Maze(arrow1)
    print(f.limits, f.start, f.goal)
    w = MazeWin(f)
    # s = bfs(f.start, f.goal_test, f.successors, w)
    dist = f.euclidian_distance()
    a = astar(f.start, f.goal_test, f.successors,
              dist, w)

    w.show_path(a)
    w.exit_on_click()