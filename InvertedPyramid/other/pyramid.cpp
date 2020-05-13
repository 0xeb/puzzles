#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <conio.h>
#include <windows.h>
using namespace std;

int pause()
{
  cout << "press any key to continue..." << endl;
  return getch();
}

int main()
{
//instructions screen & proggie info
cout << endl << " /***************************************************" << endl;
cout << "  Title: Gaby's Math Pyramid Solver" << endl;
cout << "  Author: Gabriel E. Labbad" << endl;
cout << "  E-Mail: gabrielx86@hotmail.com" << endl;
cout << "  Date: 07/24/2003 3:01am" << endl;
cout << "" << endl;
cout << "  COPYWRITE: Any replication, use, or modification of code or concept" << endl;
cout << "             herein is absolutely free as long as the original author" << endl;
cout << "             is given credit! ;)" << endl;
cout << " " << endl;
cout << "  ** Dedicated to my girlfriend Rosalie Karam (a.k.a. supert0es) **" << endl;
cout << "  ** To whom which I pray will one day be on better terms with her computer **" << endl;
cout << "  ** Plus she's always wanted a proggie or server dedicated to her! ;) **" << endl;
cout << " " << endl;
cout << "  Future Developments: If anyone finds an actual algo for solving the" << endl;
cout << "                       pyramid, instead of having the computer randomly" << endl;
cout << "                       generate the top row according to some rules and" << endl;
cout << "                       keep guessing until the correct answer is found..." << endl;
cout << "                       I'D APPRECIATE IT!  :)" << endl;

pause();

cout << " " << endl;
cout << "  Story: Last night at dinner here in Sudan a friend brought his" << endl;
cout << "         nine yr old son with him. In my attempt to humor the child I" << endl;
cout << "         gave him a math puzzle given to me by my junior high school" << endl;
cout << "         algebra teacher Ms. Valdman. I was the only child in the class" << endl;
cout << "         to solve the pyramid at 5 levels(it took 3 days with everyone" << endl;
cout << "         I can think of assisting, and the help of Lotus Spreedsheet)" << endl;
cout << "         Over a decade later I return to this friggin' puzzle to see if" << endl;
cout << "         it can go over 5 levels. I don't think it can." << endl;
cout << " " << endl;
cout << "         Enjoy the puzzle & the proggie! :)" << endl;

pause();

cout << " " << endl;
cout << " Pyramid Math Riddle... you must subtract using absolute values in the results" << endl;
cout << " going from top to bottom. You may use each number only once. You are allowed" << endl;
cout << " numbers 1 thru the summation of each level of the pyramid." << endl;
cout << " " << endl;
cout << " 2lvl pyramid  3 - 2          (allowed #'s 1 to 3)" << endl;
cout << "              =  1" << endl;
cout << " " << endl;
cout << " 3lvl pyramid 6 - 1 - 4       (allowed #'s 1 to 6)" << endl;
cout << "             =  5 - 3" << endl;
cout << "              =   2" << endl;
cout << " " << endl;
cout << " 4lvl pyramid 6 - 10 - 1 - 8  (allowed #'s 1 to 10)" << endl;
cout << "             =  4 - 9 - 7" << endl;
cout << "              =   5 - 2" << endl;
cout << "                =   3" << endl;
cout << " " << endl;
cout << " try to solve the 5 lvl pyramid by urself first!" << endl;
cout << " " << endl;
cout << " **Hint1** The largest number must go on the top level." << endl;
cout << " **Hint2** Since you subtract using absolute value the pyramids" << endl;
cout << "           mirrorable." << endl;
cout << " ***************************************************/" << endl;

    //init randomizer
    srand(unsigned(time(NULL)));

    //variables for to hold levels & size of pyramid
    int i, levels, size;

    //user inputs desired level of pyramid
    cout << endl << "Plz input pyramid levels(2 thru 5): ";
    cin  >> levels;
    size = levels;
    cout << endl;

    auto start_time = ::GetTickCount();
    //figure out the size(summation of lvls) of the pyramid
    for (i=levels; i > 0; i--)
     size += i - 1;

    int *a = new int[size+1];     //a[] holds values (1 thru n)
    bool *hbu = new bool[size+1];  //hbu[] keeps track of whether a value has been used

    bool solutionfound = false; //flag for when an answer is found

    while (!solutionfound)
    {
     solutionfound = true;        //set found to true

     //load arrays with sentinal values (all zeros)
     for (i=0; i <= size; i++)
         a[i]=0;

     //load arrays with sentinal values (all false)
     for (i=0; i <= size; i++)
         hbu[i]=false;

     //set up top row of pyramid to solve from
     //assign to spot1 highest value and then place spot1 randomly on top row somewhere
     int spot1 = rand() % levels + (size-levels+1);
     a[spot1]=size;
     hbu[size]=true; //mark highest # as used

     //fill in the rest of the top row randomly
     int topRow = levels-1;
     while (topRow > 0)
     {
      int spot = rand() % levels + (size - levels + 1);

      while (a[spot] != 0)
            spot = rand() % levels + (size - levels + 1);

      int value = rand() % size + 1;

      while (hbu[value] == true)
            value = rand() % size + 1;

      a[spot] = value;
      hbu[value] = true;

      topRow--;
     }

     //subtraction routine
     int p1,p2; //subtraction pointers
     p1=size;
     p2=size-1;

     for (int x=0; x < levels-1; x++)
     {
      for (int i=levels-x; i > 1; i--)
      {
       a[p1-levels+x]=abs(a[p1]-a[p2]);
       hbu[abs(a[p1]-a[p2])]=true;
       p1--;
       p2--;
      }
       p1--;
       p2--;
     }

     //check if solution has been found by checking to see if each number
     //has been used once
     for (int i=1; i <= size; i++)
      if (hbu[i] == false)
       solutionfound=false;
    }//end solutionfound while loop


    //pyramid print routine
    //must init a couters to print in proper visual order
    cout << endl;
    int count1 = levels;
    int count2 = levels;
    for (i=0; i < size; i++)
    {
     if (i == count2)
     {
        cout << endl;
        count1--;
        count2 = count2 + count1;

        for (int z=(levels-count1); z > 0; z--)
            cout << " ";
     }
      cout << a[size-i] << " ";
    }

    auto end_time = ::GetTickCount();

    cout << endl << endl << "Done in " << (double(end_time - start_time) / 1000.0) << " seconds" << endl;
    pause();

    delete [] a;
    delete [] hbu;
    return 0;
}